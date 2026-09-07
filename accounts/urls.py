from django.urls import path

from . import location_views, views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/', views.password_reset_request_view, name='password_reset'),
    path('password-reset/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('save-location/', location_views.save_location_view, name='save_location'),
]
