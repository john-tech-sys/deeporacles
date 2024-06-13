from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('register/', user_views.register, name='register'),

    path('login/', user_views.LoginView.as_view(), name='login'),

    path('logout/', user_views.logout_view, name='logout'),

    path('verify/<str:activation_key>', user_views.emailConfirm, name='email_confirm'),

    path('password_recover/<str:activation_key>', user_views.passwordRecover, name='password_recover'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    path('email/confirm/(<key>[0-9A-Za-z]+)/', user_views.AccountEmailActivateView.as_view(), name='email-activate'),

    path('email/resend-activation/', user_views.AccountEmailActivateView.as_view(), name='resend-activation'),
]