import json
from django.http import (JsonResponse)
from django.shortcuts import get_object_or_404
from accounts.models import User
from contrib.exceptions import SoundUploadException
from contrib.models import Comment, Like, Report, Tag
from django.db.models import Count
from home.helpers import AudioConverter, PostUploadException, PostUploader, SoundUploader
from home.views import postValidation
from django.core.paginator import Paginator
from rest_framework.decorators import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from home.models import Post, Savedpost, Sound, SoundCategory
from deeporacles.settings import (AUDIO_EXTENSIONS, MAX_AUDIO_SIZE, MAX_IMAGE_SIZE,
                             MAX_VIDEO_SIZE, VIDEO_EXTENSIONS, IMAGE_EXTENSIONS)
from .serializers import PostCommentSerializer, PostSerializer, SavedPostSerializer, SoundCategorySerializer, SoundSerializer
from django.contrib import messages

IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'gif', 'png', 'pict', 'ico', 'tiff', 'ai', 'webp', 'eps', 'cdr']
TRACK_EXTENSIONS = ['.wav', '.aif', '.mp3', '.mid']
SYMBOL_DONT_HAVE_NAME = ['#', '6', ')', '{', '=', '-', '.', ':', '%', '_', '+', '>', '5', '&', ',', '!', '@', '/', '7',
                         ']', '0', '9', '^', '8', ';', '}', '*', '|', '?', '2', '(', '3', '$', '<', '[', '1', '4', "'",
                         '"']


class Postviewset(viewsets.ModelViewSet):
    template = 'home/home.html'
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)

    def get_queryset(self):
        posts = Post.objects.filter(active=True)
        return posts


@authentication_classes(authentication.SessionAuthentication)
@permission_classes(permissions.IsAuthenticated)
@api_view(['GET',])
def posts(request, *args, **kwargs):
    # Create an empty list to store the user IDs of connections and following users
    my_connections = []

    # Step 1: Include the current user in the connections list
    my_connections.append(request.user)

    # Step 2: Include user IDs of staff users in the connections list (if the current user is staff)
    staff_users = User.objects.filter(is_staff=True)
    staff_users = list(staff_users)
    my_connections.extend(staff_users)

    # Step 3: Include user IDs of connections in the connections list
    connections = request.user.circles.connections.all()
    connections = list(connections)
    my_connections.extend(connections)

    # Step 4: Include user IDs of following users in the connections list
    following = request.user.circles.following.all()
    following = list(following)
    my_connections.extend(following)

    # Filter posts by users in the connections list
    posts = Post.objects.filter(
        active=True,
        user__in=my_connections,
    )

    # Serialize the posts and return the response
    serializer = PostSerializer(instance=posts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class Commentviewset(viewsets.ModelViewSet):
    serializer_class = PostCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Comment, id=item)

    def get_queryset(self):
        comments = Comment.objects.filter(hidden=False)
        return comments


@api_view(['POST',])
def api_create_detail_view (request):
    user = request.user
    post = Post(user=user)

    if request.method =="POST":
        serializer = PostSerializer(post, data=request.data)
        if 'Video_file' in request.FILES:
            video_file = request.FILES['Video_file']
            video = str(video_file).split('.')
            if video[1] in VIDEO_EXTENSIONS:
                if video_file.size > MAX_VIDEO_SIZE:
                    messages.error(request, 'Video file should not exceed 100 MB')
            else:
                messages.error(request,
                                'the file extension does not match the requirements. Only Video can be uploaded')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
def api_update_detail_view (request, slug):

    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save(user=request.user)
            data["success"] = "Your update was successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
def api_delete_detail_view (request, pk):

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        serializer = PostSerializer(post, data=request.data)
        operation = post.delete()
        data = {}
        if operation:
            serializer.save()
            data["success"] = "Deleted successfully"
        else:
            data["failure"] = "delete failed"
            return Response(data=data)


class PostLike(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        updated = False
        liked = False
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user in post.like.all():
            liked = False
            post.like.remove(request.user)
        else:
            liked = True
            post.like.add(request.user)
        updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


class SavePost(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        updated = False
        post_saved = False
        user = request.user
        savedpost = Savedpost.objects.get(user=request.user)
        if user.is_authenticated:
            if postValidation(request.user, post) == True:
                return JsonResponse({'blocked': True})

            elif post in savedpost.posts.all():
                savedpost.posts.remove(post)
                post_saved = False
            else:
                post_saved = True
                savedpost.posts.add(post)
            updated = True
        data = {
            "updated": updated,
            "post_saved": post_saved
        }
        return Response(data)


class ReportPost(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        updated = False
        post_reported = False
        user = request.user
        if user.is_authenticated:
            if postValidation(request.user, post) == True:
                return JsonResponse({'blocked': True})
            else:
                post_reported = True
                report, created = post.reports.get_or_create(reported_by=request.user)
                if created:
                    report.save()
            updated = True
        data = {
            "updated": updated,
            "post_reported": post_reported
        }
        return Response(data)


class VideoUploadView(APIView):
    """Handle post basic functions."""

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """Upload post to model."""
        if not request.FILES:
            raise PostUploadException('No Video file supplied.')
        return Response(
            data=PostUploader().upload(
                request.user,
                request.FILES,
                request.POST,
                request
            ),
            status=status.HTTP_201_CREATED
        )


class PostSearchView(APIView):
    """Search posts."""

    def get(self, request, *args, **kwargs):
        """
        Get paginated post search results.

        <BASE_URL>/<endpoint>/[..query_params]

        Available query_params options:
        1. page_number [int, default 1]
        2. page_size [int, default 50]
        3. search [str]

        misco.com/post/search/?search=martial%20arts&page_size=100
        """
        page_number = request.query_params.get('page_number', 1)
        page_size = request.query_params.get('page_size', 50)
        search_token = request.query_params.get('search', None)
        if not search_token:
            raise Exception('Search Token not provided.')
        posts = Post.objects.filter(
            content__icontains=search_token
        ).exclude(
            is_pornographic=True
        )
        paginator = Paginator(posts, page_size)
        serializer = PostSerializer(
            paginator.page(page_number),
            many=True,
            context={'request': request}
        )
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response


class TrendingTagPostView(APIView):
    """Display all trending posts based on tags."""

    def get(self, request, *args, **kwargs):
        """Get all trending posts based on tags."""
        popular_hashtags = Tag.objects.all().order_by('-count')[:20]
        response = {}
        for hashtag in popular_hashtags:
            posts = Post.objects.filter(
                uuid__in=Tag.objects.filter(
                    hashtag=hashtag
                ).values_list(
                    'post__uuid', flat=True
                )
            ).annotate(
                num_likes=Count('activity')
            ).order_by('-num_likes')[:10]
            response[hashtag.name] = PostSerializer(
                posts,
                many=True,
                context={'request': request}
            ).data
        return Response(
            data=response,
            status=status.HTTP_200_OK
        )


class TagFilteredPostView(APIView):
    """Get list of posts of tags."""

    def get(self, request, tag):
        """Get posts of the same tag."""
        page_number = request.query_params.get('page_number', 1)
        page_size = request.query_params.get('page_size', 50)
        tag = Tag.objects.get(name=tag.lower())
        posts = Post.objects.filter(
            uuid__in=Tag.objects.filter(
                tag=tag
            ).values_list(
                'post__uuid', flat=True
            )
        ).annotate(
            num_likes=Count('activity')
        ).order_by('-num_likes')
        paginator = Paginator(posts, page_size)
        serialized_posts = PostSerializer(
            paginator.page(page_number),
            many=True,
            context={'request': request}
        )
        return Response(
            serialized_posts.data,
            status=status.HTTP_200_OK
        )



class SoundUploadView(APIView):
    """Handle sound basic functions."""

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """Upload sound to model."""
        if not request.FILES:
            raise SoundUploadException('No Sound file supplied.')
        return Response(
            data=SoundUploader().upload(
                request.user,
                request.FILES,
                request.POST
            ),
            status=status.HTTP_201_CREATED
        )


class SoundCategorySearch(APIView):
    """Get sound based on category."""

    def get(self, request, category_id):
        """Get sounds based on category."""
        page_number = request.query_params.get('page_number ', 1)
        page_size = request.query_params.get('page_size ', 50)
        sounds = Sound.objects.filter(
            category__uuid=category_id
        )
        paginator = Paginator(sounds, page_size)
        serializer = SoundSerializer(
            paginator.page(page_number),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class SoundExtractorView(APIView):

    def get(self, request, post_uuid):
        """Extract sound of the post."""
        AudioConverter().extract(post_uuid)
        return Response(
            data={'message': 'Sound has been extracted'},
            status=status.HTTP_201_CREATED
        )

class SoundViewSet(viewsets.ModelViewSet):
    """Sound viewset for API."""

    queryset = Sound.objects.all()
    serializer_class = SoundSerializer


class SoundCategoryViewSet(viewsets.ModelViewSet):
    """Sound Category viewset for API."""

    queryset = SoundCategory.objects.all()
    serializer_class = SoundCategorySerializer
