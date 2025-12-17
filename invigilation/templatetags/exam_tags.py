# templatetags/exam_tags.py
from django import template
from django.db.models import Count
from ..models import Exam, Conflict
from django.utils import timezone
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_upcoming_exams_count():
    """Count all upcoming exams"""
    return Exam.objects.filter(exam_date__gte=timezone.now().date()).count()

@register.filter
def percentage(part, whole):
    """Calculate percentage safely"""
    try:
        return float(part) / float(whole) * 100
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def conflict_percentage(conflict):
    """Specialized percentage calculator for conflicts"""
    try:
        total = conflict.get('count', conflict.get('total', 0))
        resolved = conflict.get('resolved', 0)
        return resolved / total * 100
    except (ValueError, ZeroDivisionError):
        return 0