from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_index, name = 'notifications_index'),
    path('read/<str:notification_id>/', views.mark_read, name = 'notification_mark_read'),
]