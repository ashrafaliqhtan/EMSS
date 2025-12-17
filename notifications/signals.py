# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification

@receiver(post_save, sender=Notification)
def send_websocket_notification(sender, instance, created, **kwargs):
    if created and not instance.read:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.user.id}',
            {
                "type": "send.notification",
                "message": {
                    "id": instance.id,
                    "message": instance.message,
                    "link": instance.link,
                    "timestamp": str(instance.created_at)
                }
            }
        )