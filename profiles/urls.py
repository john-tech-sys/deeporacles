from django.urls import path

from home.views import GetPosts
from . import views as prof_views
from .views import GetArea, GetCity, GetRegion, ProfileView

urlpatterns = [
    path('my_profile', prof_views.my_profile, name='my_profile'),

    path('profile', ProfileView, name = 'profile'),
    path('get-city', GetCity, name = 'getcity'),
    path('get-region', GetRegion, name = 'getregion'),
    path('get-area', GetArea, name = 'getarea'),
    path('my_timeline/get/10-posts/<int:counts>', GetPosts, name='get-posts'),
	path('get/timeline/10-posts/<slug:profile_slug>', prof_views.getTimelinePosts, name='get-page-posts'),

	path('<int:pk>/edit/cropimg', prof_views.crop_image, name='crop_image'),
	path('<int:pk>/edit_wall/cropimg', prof_views.crop_wall_image, name='crop_wall_image'),

    path('my_profile/create_skill', prof_views.create_skill, name='create_skill'),

    path('my_profile/create_potfolio', prof_views.create_potfolio, name='create_potfolio'),

    path('my_profile/create_file', prof_views.create_file, name='create_file'),

    path('my_profile/create_wall/', prof_views.create_wall, name='create_wall'),

    path('my_timeline/', prof_views.my_timeline, name='my_timeline'),

    path('user_timeline/<slug:profile_slug>/', prof_views.user_timeline, name='user_timeline'),

    path('profile/<slug:profile_slug>/', prof_views.profile_view, name='profile_view'),

	path('carreer/<slug:slug>/', prof_views.pot_detail, name='pot_detail'),

    path('ajax/profile-picture-update/',prof_views.update_profile_picture,name='users-profile-picture-update'),

    path('ajax/profile-wall-update/',prof_views.update_wallpaper,name='users-wallpaper-update'),
]


htmx_urlpatterns = [
                    
    path('my_profile/create_education', prof_views.create_education, name='create_education'),
    
	path('delete_educ/<int:pk>', prof_views.delete_educ, name='delete_educ'),
                    
                    
]

urlpatterns += htmx_urlpatterns