from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    try:
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, ZeroDivisionError):
        return 0