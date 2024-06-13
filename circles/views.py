
from typing import Any, Dict, Union
from accounts.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.forms import CommentForm, PostCreateForm
from profiles.models import Profile
from .models import *
from .forms import * 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from home.models import Post
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from deeporacles.settings import (AUDIO_EXTENSIONS, MAX_AUDIO_SIZE, MAX_IMAGE_SIZE, IMAGE_EXTENSIONS,
                             MAX_VIDEO_SIZE, VIDEO_EXTENSIONS)
SYMBOL_DONT_HAVE_NAME = ['#', '6', ')', '{', '=', '-', '.', ':', '%', '_', '+', '>', '5', '&', ',', '!', '@', '/', '7',
                         ']', '0', '9', '^', '8', ';', '}', '*', '|', '?', '2', '(', '3', '$', '<', '[', '1', '4', "'",
                         '"']

def Forums(request):
	"""
	Renders a webpage displaying a list of active forums.
	
	Parameters:
	- request: the HTTP request object.
	
	Returns:
	- A rendered webpage showing active forums.
	"""
	forums = Forum.objects.filter(active=True)
	return render(request, 'special/group/groups.html', {'forums': forums})

@login_required
def CreateForum(request):
	"""
	Creates a new forum based on the user input in the request.
	
	Parameters:
	- request: the HTTP request object containing forum data.
	
	Returns:
	- If the form is valid, it creates a new forum and redirects to the forum page, 
	  otherwise renders the form page with errors.
	"""
	form = ForumForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			form = form.save(commit=False)
			form.forum_admin = request.user
			form.save()
			form.forum_members.add(request.user)
			form.followers.add(request.user)
			request.user.circles.forums.add(form)
			return HttpResponseRedirect((reverse('forum', args=[str(form.slug),])))
		else:
			return render(request, 'special/group/group.html', {'form': form})
	else:
		return render(request, 'special/group/group.html', {'form': form})


@login_required
def ForumSettings(request, slug):
    """
    Renders the forum settings page based on the user input in the request.

    Parameters:
    - request: the HTTP request object.
    - slug: the unique identifier of the forum.

    Returns:
    - If the HTTP request method is POST, updates the forum settings with the provided data and redirects to the current path.
    - Otherwise, renders the forum settings page with the forum information.
    """
    forum = get_object_or_404(Forum, slug=slug)
    
    if request.method == 'POST':
        if 'fname' in request.POST:
            forum.forum_name = request.POST['fname']
        if 'pic' in request.POST:
            forum.picture = request.POST['pic']
        if 'cover' in request.POST:
            forum.forum_cover_photo = request.POST['cover']
        if 'fbio' in request.POST:
            forum.forum_bio = request.POST['fbio']
        if 'fmode' in request.POST:
            forum.private_mode = request.POST['fmode']
        
        forum.save()
        return redirect(request.path_info)
    
    context = {
        'forum': forum,
        'profset_seg': True
    }
    return render(request, 'special/forum_set.html', context)


class CreatePostView(CreateView):
	model = Post
	form_class = PostCreateForm
	template_name = 'home/create_post.html'
	success_url = 'forums'

	def get_context_data(self, pk, **kwargs):
		"""
		Return the context data for the CreatePostView with the given primary key and additional keyword arguments.
		
		Parameters:
		    pk: The primary key for the context data.
		    **kwargs: Additional keyword arguments.
		    
		Returns:
		    The context data for the CreatePostView.
		"""
		context = super(CreatePostView, self).get_context_data(**kwargs)
		return context

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		"""
		Handle the POST request to create a new post. 
		Validates uploaded files (audio, image, video) against predefined size limits and extensions. 
		Checks if the post title is empty and generates an error message accordingly. 
		Calls the parent class's post method with the request, args, and kwargs.

		Parameters:
		    request: The HTTP request object.
		    *args: Additional positional arguments.
		    **kwargs: Additional keyword arguments.
		    
		Returns:
		    The result of calling the parent class's post method.
		"""
		if 'Audio_file' in self.request.FILES:
			audio_file = self.request.FILES['Audio_file']
			audio = str(audio_file).split('.')
			if audio[1] in AUDIO_EXTENSIONS:
				if audio_file.size > MAX_AUDIO_SIZE:
					messages.error(request, 'Audio file should not exceed 10 MB')
			else:
				messages.error(request,
								'the file extension does not match the requirements. Only audio can be uploaded')
		if 'picture' in self.request.FILES:
			pic = self.request.FILES['picture']
			image = str(pic).split('.')
			if image[1] in IMAGE_EXTENSIONS:
				if pic.size > MAX_IMAGE_SIZE:
					messages.error(request, 'Image file should not exceed 8 MB')
			else:
				messages.error(request,
								'the file extension does not match the requirements. Only photos can be uploaded')
		if 'Video_file' in self.request.FILES:
			video_file = self.request.FILES['Video_file']
			video = str(video_file).split('.')
			if video[1] in VIDEO_EXTENSIONS:
				if video_file.size > MAX_VIDEO_SIZE:
					messages.error(request, 'Video file should not exceed 200 MB')
			else:
				messages.error(request,
								'the file extension does not match the requirements. Only Video can be uploaded')

		content = self.request.POST['content']
		Title_post = self.request.POST['title']

		if len(Title_post.replace(' ', '')) == 0:
			messages.error(request, 'Title post cannot be empty')
		return super(CreatePostView, self).post(request, args, kwargs)

	def form_valid(self, form, pk):
		"""
		Saves the form data as a new post, associates it with a forum based on the primary key, 
		sets the user and forum attributes, saves the post, displays a success message, 
		and redirects to the success_url.

		Parameters:
		    form: The form instance containing the post data.
		    pk: The primary key used to retrieve the associated forum.
		
		Returns:
		    A redirect response to the success_url.
		"""
		post = form.save(commit=False)
		forum = Forum.objects.get(pk=pk)
		post.user = self.request.user
		post.forum = forum
		post.save()
		messages.info(self.request,
						'You successfully created a new post!')
		return redirect(self.success_url)


def ForumView(request, slug):
	page_number = request.GET.get('page', 1)
	forum = get_object_or_404(Forum, slug=slug)
	post_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=False, forum=forum).order_by('-DatePublished'), 3)
	posts = post_paginator.get_page(page_number)
	question_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=True, forum=forum).order_by('-DatePublished'), 5)
	questions = question_paginator.get_page(page_number)
	form = CommentForm()
	context = {
		'posts': posts,
		'questions': questions,
		'form': form,
		'forum': forum
	}
	context['forum_seg'] = 'forum_seg'
	return render(request, 'special/group.html', context)


def ForumMembersView(request, pk):
	forum = get_object_or_404(Forum, pk=pk)
	members = forum.forum_members.all()[:20]
	members_waiting = forum.forum_members_waiting.all()
	users = Circles.objects.exclude(user=request.user)
	other_users = []
	for m in members:
		other_users.append(m)
	for p in members_waiting:
		other_users.append(p)
	for k in other_users:
		users.exclude(user=k)
	context = {
		'users': users,
		'forum': forum,
		'members': members,
		'members_waiting': members_waiting
	}
	return render(request, 'special/group/group-members.html', context)


# connection
@login_required
def users_list(request):
	context = {}
	context['circle_seg'] = 'circle_seg'
	return render(request, "connections/circles.html", context)


def user_connection_list(
    request: HttpRequest,
    profile_slug: str,
    *args: Any,
    **kwargs: Any
) -> HttpResponse:
    """
    Renders a webpage displaying a list of connections for a given user profile.

    Parameters:
        request (HttpRequest): The HTTP request object.
        profile_slug (str): The unique identifier of the user profile.

    Returns:
        HttpResponse: The rendered webpage displaying the list of connections.
    """
    # Get the user profile based on the provided slug
    profile = Profile.objects.filter(slug=profile_slug).first()
    
    # Get the user associated with the profile
    user = profile.user
    
    # Get a list of users who are not the current user
    users = Circles.objects.exclude(user=user)
    
    # Get the list of connections for the user profile
    connections = profile.user.circles.connections.all()
    
    # Exclude the connections from the list of users
    for p in users:
        if p in connections:
            users = users.exclude(p)
    
    # Create the context dictionary for rendering the template
    context: Dict[str, Union[QuerySet[Circles], User, Profile, str]] = {
        'connections': connections,  # List of connections for the user profile
        'user': user,  # The user associated with the profile
        'profile': profile,  # The user profile
        # 'users': users,  # List of users who are not connected to the user
    }
    
    # Add the 'circle_seg' key to the context dictionary
    context['circle_seg'] = 'circle_seg'

    # Render the template with the context data
    return render(request, "connections/circles.html", context)


@login_required
def Acceptjoinrequest(request, format=None):
	forum_pk = request.data.get('forum')
	forum = Forum.objects.get(pk=forum_pk)
	user_pk = request.data.get('user')
	user = User.objects.get(pk=user_pk)

	if user not in forum.forum_members.all() and user not in forum.forum_members_blocked.all():
		forum.forum_members.add(user)
		forum.forum_members_waiting.remove(user)
	members_waiting = forum.forum_members_waiting.all()
	context = {
		'members_waiting': members_waiting
	}
	return render(request, "special/group/groupRequest.html", context)
