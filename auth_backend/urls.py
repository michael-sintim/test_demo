# authproject/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from auth_app import views as accounts_views


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', 
         auth_views.LoginView.as_view(template_name='login.html'), 
         name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(next_page='login'), 
         name='logout'),
            path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ), 
         name='password_reset_complete'),
          # User Registration and Profile
    path('register/', accounts_views.register, name='register'),
    path('edit-profile/', accounts_views.edit_profile, name='edit_profile'),
   

    path('dashboard/', accounts_views.dashboard, name='dashboard'),
    path('profile/edit/', accounts_views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', accounts_views.user_profile, name='public_profile'),
    
    # Password Change
    path('password-change/', accounts_views.change_password, name='change_password'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)