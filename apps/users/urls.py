from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name = 'logout'),
    path('register/', views.register_view, name = 'register'),
    path('follow/<int:target_id>/', views.follow_user_view, name = 'follow_user'),
    path('unfollow/<int:target_id>/', views.unfollow_user_view, name = 'unfollow_user'),
]