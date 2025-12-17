# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def mark_notification_read(request, pk):
    notification = Notification.objects.get(pk=pk, user=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'status': 'success'})

def send_notification(user, message, link=None):
    notification = Notification.objects.create(
        user=user,
        message=message,
        link=link
    )
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'send.notification',
            'message': {
                'id': notification.id,
                'message': message,
                'link': link,
                'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    )
def send_bulk_notification(users, message, link=None):
    notifications = []
    for user in users:
        notifications.append(Notification(
            user=user,
            message=message,
            link=link
        ))
    
    Notification.objects.bulk_create(notifications)
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'bulk_notifications',
        {
            'type': 'send.bulk_notifications',
            'users': [user.id for user in users],
            'message': {
                'message': message,
                'link': link,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    )
    
    
# notifications/views.py
@login_required
def notification_count(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    return JsonResponse({'count': count})    