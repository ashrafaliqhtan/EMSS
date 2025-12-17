from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_notifs',  # اسم فريد مختلف
        related_query_name='notification_notif'  # اسم فريد مختلف
    )
    # باقي الحقول...
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.message[:50]