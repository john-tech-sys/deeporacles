
from django.urls import path, include
from circles import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path
from . import views as forum_views

urlpatterns = [
	path('users/', user_views.users_list, name='users_list'),
 
	path('user_connections/<slug:profile_slug>/', user_views.user_connection_list, name='user_connection_list'),
 
#  forums
 	path('forums', forum_views.Forums, name='forums'),
  
	path('forum/<slug:slug>', forum_views.ForumView, name="forum"),
 
	path('forum/settings/<slug:slug>', forum_views.ForumSettings, name="forum_setting"),
 
	path('forum_post_create/<int:pk>', forum_views.CreatePostView.as_view(), name='forum_post_create'),
 
	path('forum-<int:pk>/members', forum_views.ForumMembersView, name='forum-members'),
 
	path('create-forum', forum_views.CreateForum, name='create-forum'),
 
	path('accept/user/forum/join/request/', forum_views.Acceptjoinrequest, name='accept-forum-request'),
]