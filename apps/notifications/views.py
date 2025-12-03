from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .services.services import get_user_notifications, mark_notification_as_read

@login_required
def notifications_index(request):
    notifications = get_user_notifications(request.user.id, limit = 10)
    return render(request, 'notifications/index.html', {'notifications': notifications})

@login_required
def mark_read(request, notification_id):
    mark_notification_as_read(notification_id)
    return redirect(request.META.get('HTTP_REFERER', 'notifications_index'))