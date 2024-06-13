

from django.db import router
from django.urls import path, include
from .circles_views import *

urlpatterns = [

    path('follow_user/api/<int:pk>', FollowAPI.as_view(), name='follow_user'),
    path('forum_api_join/api/<int:pk>', JoinRequestView.as_view(), name='forum_api_join'),
    path('follow_forum/api/<int:pk>', ForumFollowAPI.as_view(), name='forum_api_follow'),
    path('follow/api/<int:pk>', FollowAPI.as_view(), name='profile_api_follow'),
	path('accept/user/forum/join/request/', AcceptForumJoinReq.as_view(), name='accept-forum-request'),
	path('deny/user/forum/join/request/', DenyForumJoinReq.as_view(), name='deny-forum-request'),
	path('leave/forum/<int:pk>', LeaveForumView.as_view(), name="leave-forum"),
 
	path('invite/forum/member/', InviteMembers, name='invite-forum-member'),
 
]

