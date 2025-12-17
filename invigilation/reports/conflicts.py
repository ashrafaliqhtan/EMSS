# reports/conflicts.py
from datetime import date, timedelta
from django.db.models import Count
from django.utils import timezone
# استبدل:
# from .models import Conflict
# بـ:
from invigilation.models import Conflict

class ConflictReports:
    @staticmethod
    def generate_daily_report():
        """تقرير يومي عن التعارضات"""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        created_today = Conflict.objects.filter(
            created_at__date=today
        ).count()
        
        resolved_today = Conflict.objects.filter(
            resolved_at__date=today
        ).count()
        
        unresolved = Conflict.objects.filter(
            resolved=False
        ).count()
        
        by_type = Conflict.objects.filter(
            created_at__date=today
        ).values('conflict_type').annotate(
            count=Count('id')
        )
        
        return {
            'date': today,
            'created_today': created_today,
            'resolved_today': resolved_today,
            'unresolved': unresolved,
            'by_type': by_type
        }

    @staticmethod
    def generate_lecturer_conflicts_report():
        """تقرير عن المحاضرين الأكثر تعارضًا"""
        from .models import Lecturer
        
        lecturers = Lecturer.objects.annotate(
            conflict_count=Count(
                'exam_invigilator1',
                filter=Q(exam_invigilator1__conflict__resolved=False) |
                       Q(exam_invigilator2__conflict__resolved=False)
            )
        ).filter(conflict_count__gt=0).order_by('-conflict_count')[:10]
        
        return lecturers

    @staticmethod
    def generate_supervisor_conflicts_report():
        """تقرير عن المراقبين الأكثر تعارضًا"""
        from .models import ExamSupervisor
        
        supervisors = ExamSupervisor.objects.annotate(
            conflict_count=Count(
                'first_supervisor_halls',
                filter=Q(first_supervisor_halls__conflict__resolved=False) |
                       Q(second_supervisor_halls__conflict__resolved=False)
            )
        ).filter(conflict_count__gt=0).order_by('-conflict_count')[:10]
        
        return supervisors

    @staticmethod
    def generate_hall_conflicts_report():
        """تقرير عن القاعات الأكثر تعارضًا"""
        from .models import Exam
        
        halls = Exam.objects.values('exam_hall__hall_name').annotate(
            conflict_count=Count(
                'id',
                filter=Q(conflict__resolved=False)
            )
        ).filter(conflict_count__gt=1).order_by('-conflict_count')[:10]
        
        return halls