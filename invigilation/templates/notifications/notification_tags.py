# في ملف invigilation/templatetags/notification_tags.py
from django import template
from ..models import Notification

register = template.Library()

@register.simple_tag
def get_unread_notifications_count(user):
    return Notification.unread_count(user)