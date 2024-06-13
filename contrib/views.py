
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from circles.models import Forum
from home.models import Post
from . import search
from deeporacles import settings
from django.db.models import Q
from profiles.models import Profile
import itertools
from collections import Counter
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic, View
from django.views.generic import *
from contrib.models import *
from rest_framework import viewsets
from .helper import modify_response


@login_required
def NotifyHref(request, pk):
	notify = get_object_or_404(Notification, pk=pk)
	if notify.post:
		return HttpResponseRedirect((reverse('post', args=[str(notify.post.pk)])))
	else:
		return HttpResponseRedirect((reverse('profile', args=[str(notify.sender.pk)])))


def ActivatePostNotify(request, pk):
	try:
		post = Post.objects.get(pk=pk)
		if request.user in post.post_notify_people.all():
			post.post_notify_people.remove(request.user)
		else:
			post.post_notify_people.add(request.user)
		return JsonResponse({"done": "done"})
	except:
		return JsonResponse({"error": "Whops something went wrong, or the object has been deleted."})

class PostNotification(View):
	def get(self, request, notification_pk, post_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		post = Post.objects.get(pk=post_pk)

		notification.is_seen = True
		notification.save()

		return redirect('details', pk=post_pk)

class ProfileNotification(View):
	def get(self, request, notification_pk, profile_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		profile = Profile.objects.get(pk=profile_pk)

		notification.is_seen = True
		notification.save()

		return redirect('profile_view', pk=profile_pk)


def delete(request, notification_pk, *args, **kwargs):
	notification = Notification.objects.get(pk=notification_pk)

	notification.is_seen = True
	notification.save()
	receiver = request.user
	notifications = Notification.objects.filter(receiver=receiver, is_seen=False)
	return render(request, 'notification/snippet.html', {'notifications': notifications})


def view_all_notifs(request, *args, **kwargs):
	receiver = request.user
	notifications = Notification.objects.filter(receiver=receiver)
	for notification in notifications:
		if not notification.is_seen:
			notification.is_seen = True
			notification.save()
	notifications = Notification.objects.filter(receiver=receiver, is_seen=False)
	return render(request, 'notification/snippet.html', {'notifications': notifications})


def general_results(request):
    q = request.GET.get('q')
    s_posts = Post.objects.filter(Q(title__icontains=q))
    s_profiles =  Profile.objects.filter(Q(last_name__icontains=q) |
        Q(first_name__icontains=q) |
        Q(middle_name__icontains=q) |
        Q(user__username__icontains=q))
    s_forums =  Forum.objects.filter(Q(forum_name__icontains=q))
    # store the search
    search.store(request, q)
    page_title = 'Deep Oracles General Search Results for: ' + q
    return render(request, "search/general_results.html", locals())


# def general_results(request):
#     q = request.GET.get('q')
#     s_posts = Post.objects.filter(Q(title__icontains=q))
#     s_profiles =  Profile.objects.filter(Q(last_name__icontains=q) |
#         Q(first_name__icontains=q) |
#         Q(middle_name__icontains=q) |
#         Q(user__username__icontains=q))
#     # store the search
#     search.store(request, q)
#     page_title = 'Deep Oracles General Search Results for: ' + q
#     return render(request, "search/general_results.html", locals())


# def SearchView(request):
class ViewSet(viewsets.ViewSet):
    """
    Overriding : Modify the API response format for common place.
    """

    def initial(self, request, *args, **kwargs):
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        response = modify_response(response)
        return super().finalize_response(request, response, *args, **kwargs)

    def get_serializer_context(self):
        """
        Set client IP Address and request url in the context
        """
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context
