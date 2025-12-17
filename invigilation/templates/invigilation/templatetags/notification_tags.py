# invigilation/templatetags/notification_tags.py
from django import template
from invigilation.models import Notification  # التصحيح هنا
# from invigilation.templatetags.models import Notification ❌ خطأ

register = template.Library()

@register.simple_tag
def get_unread_notifications_count(user):
    return Notification.objects.filter(user=user, read=False).count()