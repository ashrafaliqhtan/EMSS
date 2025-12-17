# templatetags/exam_tags.py
from django import template
from ..models import Exam
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_upcoming_exams_count():
    return Exam.objects.filter(exam_date__gte=timezone.now().date()).count()