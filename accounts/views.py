
from django.dispatch.dispatcher import receiver

from django.http.response import Http404, JsonResponse
from django.urls.base import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods, require_safe
from utils.mixins import NextUrlMixin, RequestFormAttachMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .forms import *
# from .models import EmailActivation


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
	form_class = LoginForm
	template_name = 'accounts/login.html'
	default_next = '/'

	def get_success_url(self):
		return self.get_next_url()

	def form_valid(self, form):
		next_path = self.get_next_url()
		return redirect(next_path)


@require_safe
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out! Hope to see you again")
    return redirect('home')



def register(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))
	context = {}
	if request.POST:
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['form'] = form

	else:
		form = UserRegisterForm()
		context['form'] = form
	return render(request, 'accounts/register.html', context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


class AccountEmailActivateView(FormMixin, View):
    success_url = '/authenticate/login'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login") 
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user 
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)

def emailConfirm(request, activation_key):
	euser = get_object_or_404(EmailConfirmed, activation_key = activation_key)
	if euser is not None:
		euser.email_confirmd = True
		euser.save()
		
		user1 = User.objects.get(email = euser)
		user1.is_active = True
		user1.save()
		return render(request, 'accounts/success.html')

def passwordRecover(request, activation_key):
	if request.method == 'POST':
		if 'new-password' in request.POST:
			user = User.objects.get(email = request.POST['user_email'])
			user.set_password(request.POST['new-password'])
			user.save()
			messages.success(request, 'Password set successfully. Please login..')
			return redirect('login')
	else:
		euser = get_object_or_404(EmailConfirmed, activation_key = activation_key)
		if euser is not None:
			euser.email_confirmd = True
			euser.save()
			user1 = User.objects.get(email = euser)
			user1.is_active = True
			user1.save()
			return render(request, 'accounts/newpass.html', {'user_email': euser})