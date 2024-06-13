from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from settings.models import EmailConfig
from .models import *
from django.http import JsonResponse
from django.views import View
from .models import NewsletterEmail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
# Create your views here.

def faq(request, *args, **kwargs):
    faq = Faq.objects.all()
    return render(request, 'noticeboard/FAQ.html', {'faq': faq})

def startselling(request, *args, **kwargs):
    info = Startselling.objects.filter(active=True)
    return render(request, 'noticeboard/startselling.html', {'info': info})


def safetytips(request, *args, **kwargs):
    safetytips = SafetyTips.objects.all()
    return render(request, 'PTS/safetytips.html', {'safetytips': safetytips})


def terms(request, *args, **kwargs):
    terms = Terms.objects.filter(active=True)
    return render(request, 'PTS/terms.html', {'terms': terms})


class AddNewsletterEmail(View):
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        if not NewsletterEmail.objects.filter(email = email).exists():
            nlemail = NewsletterEmail(
                email=email
            )
            nlemail.request = request
            nlemail.save()
            type = 'add'
            try:
                return JsonResponse({'type': type})
            finally:
                email_config = EmailConfig.objects.get()
                subject, from_email, to = 'Welcome to newsletter', email_config.email_host_user, email
                text_content = 'Welcome to newsletter.'
                html_content = render_to_string('newsletter/welcome-newsletter.html', context={
                    'domain': get_current_site(request).domain
                })
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        else:
            type = 'exist'
            return JsonResponse({'type': type})
