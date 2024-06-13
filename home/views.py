import logging
import random
from circles.models import Forum
from deeporacles.settings import (AUDIO_EXTENSIONS, MAX_AUDIO_SIZE, MAX_IMAGE_SIZE,
                             MAX_VIDEO_SIZE, VIDEO_EXTENSIONS, IMAGE_EXTENSIONS)
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import  HttpRequest, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from contrib.models import Comment, Notification
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .forms import CommentForm, PostCreateForm
from .models import Post, PostView, Savedpost, Share, Space
import pytz
SYMBOL_DONT_HAVE_NAME = ['#', '6', ')', '{', '=', '-', '.', ':', '%', '_', '+', '>', '5', '&', ',', '!', '@', '/', '7',
                         ']', '0', '9', '^', '8', ';', '}', '*', '|', '?', '2', '(', '3', '$', '<', '[', '1', '4', "'",
                         '"']
# Create your views here.

logger = logging.getLogger(__name__)




def error_404(request, exception=None):
	title = 'Error_404'
	return render(request, 'home/404.html', {'exception': exception}, status=404)


def custom_500_view(request):
    return render(request, 'home/500.html', status=500)



def home(request, *args, **kwargs):
	page_number = request.GET.get('page', 1)
	if request.user.is_authenticated:
		post_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=False).order_by('-DatePublished'), 5)
		posts = post_paginator.get_page(page_number)
		# posts = Post.objects.filter((Q(user = request.user) | 
		# 						Q(user__in = request.user.circles.connections.all()) | 
		# 						Q(user__in = request.user.circles.following.all()) | 
		# 						Q(forum__in = request.user.circles.forums.all())), hidden=False).order_by('-DatePublished')[counter:][:4]
	else:
		post_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=False).order_by('-DatePublished'), 5)
		posts = post_paginator.get_page(page_number)
	question_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=True).order_by('-DatePublished'), 5)
	questions = question_paginator.get_page(page_number)
	form = CommentForm()
	context = {
		'posts':posts,
		'questions':questions,
		'form': form,
	}
	context['segment'] = 'home'
	template = 'home/home.html'

	return render(request, template, context)


def SpaceView(request, slug):
	page_number = request.GET.get('page', 1)
	space = get_object_or_404(Space, slug=slug)
	post_paginator = Paginator(Post.objects.filter(space=space, hidden=False, active=True, is_question=False).order_by('-DatePublished'), 6)
	posts = post_paginator.get_page(page_number)
	form = CommentForm()
	context = {
	'form': form,
	'space': space,
	'posts': posts,
	}
	context['segment'] = 'Space'
	return render(request, 'home/space.html', context)


def QuestionView(request):
	page_number = request.GET.get('page', 1)
	question_paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=True).order_by('-DatePublished'), 6)
	questions = question_paginator.get_page(page_number)
	context = {
	'questions': questions,
	}
	return render(request, 'home/questions_page.html', context)



# def load_more_posts(request):
#     page = request.GET.get('page', 1)
#     posts_list = Post.objects.filter(hidden=False, active=True, is_question=False).order_by('-DatePublished')
#     paginator = Paginator(posts_list, 2)  # 10 posts per page

#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)

#     context = {'posts': posts}
#     return render(request, 'home/posts.html', context)

def load_more_questions(request):
    page = request.GET.get('page', 1)
    questions_list = Post.objects.filter(hidden=False, active=True, is_question=True).order_by('-DatePublished')
    paginator = Paginator(questions_list, 2)  # 10 questions per page

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = {'questions': questions}
    return render(request, 'home/questions.html', context)


def load_more_posts(request):
    """
    Fetch paginated articles and render them.
    """
    page_number = request.GET.get('page', 1)
    paginator = Paginator(Post.objects.filter(hidden=False, active=True, is_question=False).order_by('-DatePublished'), 3)
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/posts.html', {'posts': page_obj})


def GetPostComment(request, pk, counts):

	try:
		post = Post.objects.get(pk=pk)
		comments = post.comments.all()[counts:][:2]
		rendered = []
		for comment in comments:
			serializer = render_to_string('fragments/snippets/comment.html', {'comment': comment})
			rendered.append(serializer)
		return JsonResponse(rendered, safe=False)

	except:
		return JsonResponse({'message':"Whops something went wrong or the objects has been deleted!"})


def GetPosts(request, counts = 0):
	posts = Post.objects.filter()[counts:][:2]
	form = CommentForm()
	if not posts:
		return JsonResponse({'message':"No more content to display!"})
	else:
		data = []
		for post in posts:
			posst = render_to_string("home/posts.html", {'post': post, 'form':form} , request)
			data.append(posst)
		return JsonResponse(data, safe=False)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment_form = CommentForm()
    comments = post.comments.all().order_by('comment_date')

    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'num_comments': len(comments)
    }
    context['segment'] = 'home'
    if request.user.is_authenticated:
        PostView.objects.get_or_create(post=post, user=request.user)
    post.view_count += 1
    post.save()
    return render(request, "home/post_detail.html", context)


class CreatePostView(CreateView):
	model = Post
	form_class = PostCreateForm
	template_name = 'home/create_post.html'
	success_url = 'home'

	def get_context_data(self, **kwargs):
		context = super(CreatePostView, self).get_context_data(**kwargs)
		context['title'] = 'Create Post'
		context['h1'] = 'Create Post Form'
		context['segment'] = 'home'
		return context

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		if 'Audio_file' in self.request.FILES:
			audio_file = self.request.FILES['Audio_file']
			audio = str(audio_file).split('.')
			if audio[1] in AUDIO_EXTENSIONS:
				if audio_file.size > MAX_AUDIO_SIZE:
					messages.error(request, 'Audio file should not exceed 5 MB')
			else:
				messages.error(request,
								'the file extension does not match the requirements. Only audio can be uploaded')
		if 'picture' in self.request.FILES:
			pic = self.request.FILES['picture']
			image = str(pic).split('.')
			if image[1] in IMAGE_EXTENSIONS:
				if pic.size > MAX_IMAGE_SIZE:
					messages.error(request, 'Image file should not exceed 3 MB')
			else:
				messages.error(request,
								'the file extension does not match the requirements. Only photos can be uploaded')
		if 'Video_file' in self.request.FILES:
			video_file = self.request.FILES['Video_file']
			video = str(video_file).split('.')
			if video[1] in VIDEO_EXTENSIONS:
				if video_file.size > MAX_VIDEO_SIZE:
					messages.error(request, 'Video file should not exceed 20 MB')
			else:
				messages.error(request,
								'the file extension does not match the requirements. Only Video can be uploaded')

		content = self.request.POST['content']
		Title_post = self.request.POST['title']
		forum_post = self.request.POST['forum']
		space_post = self.request.POST['space']

		if len(Title_post.replace(' ', '')) == 0:
			messages.error(request, 'Title post cannot be empty')
		return super(CreatePostView, self).post(request, args, kwargs)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.user = self.request.user
		post.author = self.request.user
		post.save()
		messages.info(self.request,
						'You successfully created a new post!')
		return redirect(self.success_url)


class AskQuestionView(CreateView):
	model = Post
	form_class = PostCreateForm
	template_name = 'home/ask_question.html'
	success_url = 'home'

	def get_context_data(self, **kwargs):
		context = super(AskQuestionView, self).get_context_data(**kwargs)
		context['title'] = 'Ask Question'
		context['h1'] = 'Ask Question'
		context['segment'] = 'home'
		return context

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		content = self.request.POST['content']
		Title_post = self.request.POST['title']
		forum_post = self.request.POST['forum']
		if len(Title_post.replace(' ', '')) == 0:
			messages.error(request, 'Title post cannot be empty')
		return super(AskQuestionView, self).post(request, args, kwargs)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.user = self.request.user
		post.is_question = True
		post.save()
		messages.info(self.request,
						'You successfully created a new post!')
		return redirect(self.success_url)


@require_http_methods(['DELETE'])
def delete_post(request: HttpRequest, pk: int) -> HttpResponse:
	"""
	Delete a task given its primary key.

	Args:
		request (HttpRequest): The request object.
		pk (int): The primary key of the task to delete.

	Returns:
		HttpResponse: A redirect to the questions page.
	"""
	counter = request.GET.get("counter" or None)
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	posts = Post.objects.filter(hidden=False, active=True, is_question=False).order_by('-DatePublished')[counter:][:2]
	return render(request, 'home/posts.html', {'posts': posts})


@require_http_methods(['DELETE'])
def delete_question(request: HttpRequest, pk: int) -> HttpResponse:
	"""
	Delete a task given its primary key.

	Args:
		request (HttpRequest): The request object.
		pk (int): The primary key of the task to delete.

	Returns:
		HttpResponse: A redirect to the questions page.
	"""
	counter = request.GET.get("counter" or None)
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	questions = Post.objects.filter(hidden=False, active=True, is_question=True).order_by('-DatePublished')[counter:][:2]
	return render(request, 'home/questions.html', {'questions': questions})


def postValidation(user, post):
	if post.forum and user in post.forum.forum_members_blocked.all():
		return True
	elif post.forum and post.forum.private_mode and user not in post.forum.forum_members.all():
		return True
	elif user in post.user.profile.blocked.all():
		return True
	elif post.user in user.profile.blocked.all():
		return True
	else:
		return False


@login_required
def comment(request, pk):
	if request.POST:
		try:
			post = Post.objects.get(pk=pk)
		except:
			return JsonResponse({'success':False})
		comment = request.POST.get('comment')
		comment = Comment.objects.create(content_object=post, user=request.user, comment=comment)
		absolute_url = "/{0}".format(post.get_absolute_url)
		text_preview = "{0} commented on your post {1}".format(comment.user, post.title)
		Notification.objects.create(sender=comment.user, text_preview=text_preview, receiver=post.user, content_object=comment, redirect_url=absolute_url)
		form = render_to_string('home/fragments/ajax_comment.html', {'comment': comment} , request)
		return JsonResponse({'comment': form,})
	return render(request, 'home/home.html')


# @login_required
# def create_comment(request, content_type_id=None, object_id=None, post_id=None):
#     print("create_comment view called")  # Debugging statement
#     if post_id:
#         post = get_object_or_404(Post, pk=post_id)
#         obj = post
#         content_type = ContentType.objects.get_for_model(Post)
#     else:
#         content_type = get_object_or_404(ContentType, pk=content_type_id)
#         obj = content_type.get_object_for_this_type(pk=object_id)

#     if request.method == 'POST':
#         print("POST request received")  # Debugging statement
#         comment_text = request.POST.get('comment')
#         if comment_text:
#             comment = Comment.objects.create(content_object=obj, user=request.user, comment=comment_text)
#             print(f"Comment created: {comment.id}")  # Debugging statement
#             return render(request, 'home/fragments/comment.html', {'comment': comment})
#         else:
#             form = CommentForm(request.POST, request.FILES)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.user = request.user
#                 comment.content_object = obj
#                 comment.save()
#                 print(f"Comment created via form: {comment.id}")  # Debugging statement
#                 return HttpResponseRedirect(obj.get_absolute_url())
#     else:
#         form = CommentForm()

#     return render(request, 'home/fragments/comment.html', {'form': form, 'post': obj})


@require_http_methods(['DELETE'])
def delete_response(request: HttpRequest, pk: int) -> HttpResponse:
    counter = request.GET.get('counter', None)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    comments = Comment.objects.filter(hidden=False).order_by('-comment_date')[counter:counter+20]
    return render(request, 'home/fragments/comment.html', {'comments': comments})


@login_required
def SavePost(request):
	savedpost = Savedpost.objects.get(user=request.user)
	saved_posts = []
	saved_questions = []
	for post_saved in savedpost.posts.all():
		if post_saved.is_question and post_saved.active and not post_saved.hidden:
			saved_questions.append(post_saved)
		elif not post_saved.is_question and post_saved.active and not post_saved.hidden:
			saved_posts.append(post_saved)
	page_number = request.GET.get('page', 1)
	question_paginator = Paginator(saved_questions, 5)
	questions = question_paginator.get_page(page_number)
	post_paginator = Paginator(saved_posts, 5)
	posts = post_paginator.get_page(page_number)
	form = CommentForm()		
	context = {
		'form': form,
		'posts': posts,
		'questions': questions,
		'segment': 'Saved',
	}
	context['segment'] = 'Bucket'
	return render(request, 'profiles/my_timeline.html', context)


@login_required
def reviews(request, view=None, *args, **kwargs):
	user = request.user
	# Filter posts based on comments made by the user and whether it's a question
	posts_with_comments = Post.objects.filter(comments__user=user, is_question=False).distinct()
	questions_with_comments = Post.objects.filter(comments__user=user, is_question=True).distinct()

	form = CommentForm()		
	context = {
		'form': form,
		'posts': posts_with_comments,
		'questions': questions_with_comments,
		'segment': 'Reviews',
	}
	context['segment'] = 'Reviews'

	return render(request, 'profiles/my_timeline.html', context)


@login_required
def posts_viewed(request):
    """
    View function to return all the posts viewed by a request.user.
    Separate between posts and questions using a boolean field in the post model called is_question.
    """
    try:
        posts_viewed = PostView.objects.filter(user=request.user)
        posts = []
        questions = []
        for post_view in posts_viewed:
            if post_view.post.is_question:
                questions.append(post_view)
            else:
                posts.append(post_view)
        context = {
            'posts': posts,
            'questions': questions,
            'segment': 'Recentviews',
        }
        return render(request, 'profiles/my_timeline.html', context)
    except PostView.DoesNotExist:
        logger.error('PostView does not exist for the user.')
        return HttpResponseNotFound(render(request, 'home/404.html'))
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}', exc_info=True)
        return HttpResponseNotFound(render(request, 'home/404.html'))


@login_required
def recommend_post(request):
    """
    Recommend a post or question to a user based on recent views, saved posts, and comments.
    """
    user = request.user

    # Get the content of the posts viewed, saved, and commented on by the user
    viewed_titles = PostView.objects.filter(user=user).values_list('post__title', flat=True)
    viewed_contents = PostView.objects.filter(user=user).values_list('post__content', flat=True)
    saved_titles = user.profile.saved_posts.values_list('title', flat=True)
    saved_contents = user.profile.saved_posts.values_list('content', flat=True)
    commented_titles = Post.objects.filter(comments__user=user).values_list('title', flat=True)
    commented_contents = Post.objects.filter(comments__user=user).values_list('content', flat=True)

    # Filter out None values
    title_queries = list(filter(None, viewed_titles)) + list(filter(None, saved_titles)) + list(filter(None, commented_titles))
    content_queries = list(filter(None, viewed_contents)) + list(filter(None, saved_contents)) + list(filter(None, commented_contents))

    # Check if there are any valid titles or contents to search for
    if not title_queries and not content_queries:
        context = {
            'questions': None,
            'posts': None,
            'segment': 'Recommendation',
        }
        return render(request, 'profiles/my_timeline.html', context)

    # Build the query
    relevant_posts = Post.objects.filter(
        Q(title__icontains=" ".join(title_queries)) |
        Q(content__icontains=" ".join(content_queries))
    )

    # Exclude posts already viewed by the user
    not_viewed_posts = relevant_posts.exclude(postview__user=user)

    # Select a random post if available
    recommended_post = random.choice(list(not_viewed_posts)) if not_viewed_posts.exists() else None

    # Initialize variables
    questions = posts = None

    if recommended_post:
        if recommended_post.is_question:
            questions = recommended_post
        else:
            posts = recommended_post

    context = {
        'questions': questions,
        'posts': posts,
        'segment': 'Recommendation',
    }

    return render(request, 'profiles/my_timeline.html', context)



@login_required
def SharingPost(request, pk):
	try:
		post = Post.objects.get(pk=pk)
		forum_pk = request.POST.get('forum_pk' or None)
		content = request.POST.get('content' or None)
		title = request.POST.get('title' or None)
		if not forum_pk is None:
			try:
				forum = Forum.objects.get(pk=forum_pk)
				shared_post = Post.objects.create(user=request.user, share=post.share or post, content=content , forum=forum)
				shares = post.shared.all()
				if shares.count() == 1:
					counts = 1 + " Share"
				else:
					counts = shares.count() + " Shares"
				post.shared.add(request.user)
				if post.share:
					post.share.shared.add(request.user)
				return JsonResponse({'counts' : counts})
			except:
				return JsonResponse({"data": "Whops! something went wrong or the post has been deleted."})
		else:
			shared_post = Post.objects.create(user=request.user, title=title, content=content, shared=post.share)
			shares = post.shared.all()
			if shares.count() == 1:
				counts = "1 Share"
			else:
				counts = "%d Shares"% shares.count()
			post.shared.add(request.user)
			if post.share:
					post.share.shared.add(request.user)
			return JsonResponse({'counts' : counts})
	except:
		return JsonResponse({"data": "Whops! something went wrong or the post has been deleted."})


def set_timezone(request):
	if request.method == 'POST':
		request.session['django_timezone'] = request.POST['timezone']
		return redirect('/')
	else:
		return render(request, 'home/template.html', {'timezones': pytz.common_timezones})



def PostMiddleRender(request, post):
	return render_to_string('home/post-middle.html', {'post': post}, request)

@login_required
def RemovePostReact(request, pk):
	post = Post.objects.get(pk=pk)

	if request.user in post.like.all():
		post.like.remove(request.user)

	elif request.user in post.love.all():
		post.love.remove(request.user)

	elif request.user in post.haha.all():
		post.haha.remove(request.user)

	elif request.user in post.sad.all():
		post.sad.remove(request.user)

	elif request.user in post.wow.all():
		post.wow.remove(request.user)

	elif request.user in post.angry.all():
		post.angry.remove(request.user)

	else:
		pass

	post.save()

	return JsonResponse(PostMiddleRender(request, post), safe=False)


@login_required
def LikePost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})

	elif request.user in post.like.all():
		post.like.remove(request.user)
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.like.add(request.user)
		return JsonResponse(PostMiddleRender(request, post), safe=False)


@login_required
def LovePost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.love.all():
		post.love.remove(request.user)
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.love.add(request.user)
		return JsonResponse(PostMiddleRender(request, post), safe=False)


@login_required
def SmilePost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.haha.all():
		post.haha.remove(request.user)
		post.save()
		print(post.reacts_count())
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.haha.add(request.user)
		return JsonResponse(PostMiddleRender(request, post), safe=False)


@login_required
def SadPost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.sad.all():
		post.sad.remove(request.user)
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.sad.add(request.user)
		return JsonResponse(PostMiddleRender(request, post), safe=False)

@login_required
def WowPost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.wow.all():
		post.wow.remove(request.user)
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.wow.add(request.user)
		return JsonResponse(PostMiddleRender(request, post), safe=False)

@login_required
def AngryPost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.angry.all():
		post.angry.remove(request.user)
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.angry.add(request.user)
		return JsonResponse(PostMiddleRender(request, post), safe=False)
