
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import handler404, handler500
from home.views import custom_500_view, error_404



schema_view = get_schema_view(
   openapi.Info(
      title="Deep Oracles API",
      default_version='v1',
      description="Deep Oracles API description",
      terms_of_service="https:localhost:8000/terms",
      contact=openapi.Contact(email="deeperoracles@gmail.com"),
   ),
   public=False,
   permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
   path('swagger<format>.json|.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Main Admin
   path('deeporacles/admin', admin.site.urls),

    #  Plugin urls
   path('froala_editor/',include('froala_editor.urls')),
   path('accounts/', include('allauth.urls')),

    # App urls 

   path('', include('home.urls')),
   path('authenticate/', include('accounts.urls')),
   path('profiles/', include('profiles.urls')),
   path('circles/', include('circles.urls')),
   path('noticeboard/', include('noticeboard.urls')),
   path('ajoinfo/', include('deepinfo.urls')),
   path('mypal/', include('mypal.urls')),
   path('contrib/', include('contrib.urls')),

   # APIS

   # REST_FRAMEWORK URLS
   path('api-auth/', include('rest_framework.urls')),
   # path('rest-auth/', include('rest_auth.urls')),
   path('auth/', include('djoser.urls.jwt')),
   # path('rest-auth/registration/', include('rest_auth.registration.urls')),

   #  Project API

    path('main_api/', include('home.api.urls')),

    path('accounts_api/', include('accounts.api.urls')),

    path('circles_api/', include('circles.api.urls')),

    path('profile_api/', include('profiles.api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = error_404

handler500 = custom_500_view