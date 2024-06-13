from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.models import User
from .models import *
from django.db.models import Q
from deeporacles import settings
from .forms import ContactForm, Admin_MessageForm
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.

def about(request, *args, **kwargs):
    abouts = Aboutus.objects.all()
    return render(request, 'deepinfo/about_us.html', locals())


def contact(request, *args, **kwargs):
    title = 'Contact us now'
    form = ContactForm(request.POST or None)
    confirm_message = None

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = 'message from deeporacles.com'
        message = '%s %s' %(comment, name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
        title = "Thanks!"
        confirm_message = "Thanks for the message. We will get right bak to you."
        form = None

    context = {'title': title, 'form': form, 'confirm_message': confirm_message}
    return render(request, 'deepinfo/contact_us.html', context)


@login_required
def AdminMessageView(request, partner_id):
	partner = get_object_or_404(User, pk=partner_id)
	messages 	= Admin_Message.objects.filter((Q(sender=request.user, receiver=partner)| Q(receiver = request.user, sender=partner))).order_by('date')
	sideMessages = [Admin_Message.objects.filter((Q(sender=request.user, receiver=user)| Q(receiver = request.user, sender=user))).last() for user in request.user.profile.chatted_with.all()]
	form 		= Admin_MessageForm()
	context 	= {'messages': messages, 'form':form, 'partner':partner}

	if sideMessages:
		for m in sideMessages:
			if not m:
				sideMessages.remove(m)
		context['side_messages'] = sideMessages

	return render(request, 'deepinfo/admin_messages.html', context)
	