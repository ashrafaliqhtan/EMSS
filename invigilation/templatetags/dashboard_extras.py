# invigilation/templatetags/dashboard_extras.py
from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value, total):
    try:
        if total == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, ZeroDivisionError):
        return 0