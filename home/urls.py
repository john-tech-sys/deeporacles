from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views
from contrib import views as search_views


urlpatterns = [

	path('post_create/', CreatePostView.as_view(), name='post_create'),
	path('ask_question/', AskQuestionView.as_view(), name='ask_question'),

	path('', views.home, name='home'),
 
	path('get/10-comments/on/post-number/<int:pk>/<int:counts>', views.GetPostComment, name='get-comments'),
	path('get/10-posts/<int:counts>', views.GetPosts, name='get-posts'),
    # path('<slug:slug>', PageView.as_view(), name='page'),

	path('load_more_questions', views.load_more_questions, name="load_more_questions"),
	path('load_more_posts', views.load_more_posts, name="load_more_posts"),
	path('questions>', views.QuestionView, name="questions"),

	path('space/<slug:slug>', views.SpaceView, name="space"),
 
	path('details/<slug:slug>', views.post_detail, name='details'),

	path('comment/<int:pk>', views.comment, name='comment'),
 
	path('delete_response/<int:pk>', views.delete_response, name='delete_response'),

	path('save_posts/', views.SavePost, name='save-post'),

    path('posts_viewed/', views.posts_viewed, name='posts_viewed'),

    path('reviews/', views.reviews, name='reviews'),

    path('recommend_post/', views.recommend_post, name='recommend_post'),
    
	path('share/post/<int:pk>', views.SharingPost, name='share-posts'),

    path('404', error_404, name='404'),

    path('timezone', views.set_timezone, name='set_timezone'),

    path('posts/<int:pk>/delete/', delete_post, name='delete_post'),

    path('questions/<int:pk>/delete/', delete_question, name='delete_question'),

	# search

    path('general_results/', search_views.general_results, name='search_general_results'),
	##Reacting
	path('remove-react/on/post-number/<int:pk>', views.RemovePostReact, name='remove-post-react'),

	path('like/post-number/<int:pk>', views.LikePost, name='like-post'),
	path('love/post-number/<int:pk>', views.LovePost, name='love-post'),
	path('haha/post-number/<int:pk>', views.SmilePost, name='haha-post'),
	path('sad/post-number/<int:pk>', views.SadPost, name='sad-post'),
	path('angry/post-number/<int:pk>', views.AngryPost, name='angry-post'),
	path('wow/post-number/<int:pk>', views.WowPost, name='wow-post'),
	
]