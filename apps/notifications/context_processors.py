from notifications.services.services import count_unread_notifications

def notification_count(request):
    if request.user.is_authenticated:
        count = count_unread_notifications(request.user.id)
        return {'unread_notifications_count': count}
    return {}