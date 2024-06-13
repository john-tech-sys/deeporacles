 

from django.db import router
from django.urls import path, include
from .home_views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('comments', Commentviewset, basename='comments')
router.register('post_viewset', Postviewset, basename='post_viewset')


urlpatterns = [

    path('', include(router.urls)),

    path('posts', posts, name='posts'),

    path('<slug:slug>/update', api_update_detail_view, name="update"),

    path('<int:pk>/delete', api_delete_detail_view, name="delete"),

    path('create', api_create_detail_view, name="create"),

    path('post/like/api/<int:pk>', PostLike.as_view(), name='post_api_like'),

    path('post/save/api/<int:pk>', SavePost.as_view(), name='post_api_save'),

    path('post/report/api/<int:pk>', ReportPost.as_view(), name='post_api_report'),

    path('post/video/create', VideoUploadView.as_view(), name='post_api_video'),

    path('post/search/posts', PostSearchView.as_view(), name='post_api_search'),

    path('post/report/api/tags', TrendingTagPostView.as_view(), name='post_api_tags'),
]
