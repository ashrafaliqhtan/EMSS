# utils/conflicts.py
from django.db.models import Q
from datetime import datetime, time
from .models import Conflict, Exam, ExamHallAssignment

class ConflictUtils:
    @staticmethod
    def detect_all_conflicts():
        """الكشف عن جميع التعارضات المحتملة في النظام"""
        # تعارضات المحاضرين في الامتحانات
        exam_conflicts = Exam.objects.annotate(
            invigilator1_count=Count('invigilator1__exam_invigilator1'),
            invigilator2_count=Count('invigilator2__exam_invigilator2')
        ).filter(
            Q(invigilator1_count__gt=1) | Q(invigilator2_count__gt=1)
        )
        
        # تعارضات المراقبين في تخصيص القاعات
        assignment_conflicts = ExamHallAssignment.objects.annotate(
            supervisor1_count=Count('first_supervisor__first_supervisor_halls'),
            supervisor2_count=Count('second_supervisor__second_supervisor_halls')
        ).filter(
            Q(supervisor1_count__gt=1) | Q(supervisor2_count__gt=1)
        )
        
        # تعارضات القاعات
        hall_conflicts = Exam.objects.values('exam_hall', 'exam_date', 'exam_period').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        return {
            'exam_conflicts': exam_conflicts,
            'assignment_conflicts': assignment_conflicts,
            'hall_conflicts': hall_conflicts
        }

    @staticmethod
    def get_lecturer_conflicts(lecturer):
        """الحصول على جميع التعارضات لمحاضر معين"""
        conflicts = []
        
        # تعارضات في الامتحانات
        exam_conflicts = Exam.objects.filter(
            (Q(invigilator1=lecturer) | Q(invigilator2=lecturer))
        ).values('exam_date', 'exam_period').annotate(
            count=Count('id'),
            exam_names=ArrayAgg('exam_name')
        ).filter(count__gt=1)
        
        for conflict in exam_conflicts:
            conflicts.append({
                'type': 'exam',
                'date': conflict['exam_date'],
                'period': conflict['exam_period'],
                'count': conflict['count'],
                'details': conflict['exam_names']
            })
        
        return conflicts

    @staticmethod
    def get_supervisor_conflicts(supervisor):
        """الحصول على جميع التعارضات لمراقب معين"""
        conflicts = []
        
        # تعارضات في تخصيص القاعات
        assignment_conflicts = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor))
        ).values('exam_date', 'exam_period').annotate(
            count=Count('id'),
            courses=ArrayAgg('course_code')
        ).filter(count__gt=1)
        
        for conflict in assignment_conflicts:
            conflicts.append({
                'type': 'assignment',
                'date': conflict['exam_date'],
                'period': conflict['exam_period'],
                'count': conflict['count'],
                'details': conflict['courses']
            })
        
        return conflicts

    @staticmethod
    def get_hall_conflicts(hall):
        """الحصول على جميع التعارضات لقاعة معينة"""
        conflicts = []
        
        # تعارضات في الامتحانات
        exam_conflicts = Exam.objects.filter(
            exam_hall=hall
        ).values('exam_date', 'exam_period').annotate(
            count=Count('id'),
            exam_names=ArrayAgg('exam_name')
        ).filter(count__gt=1)
        
        for conflict in exam_conflicts:
            conflicts.append({
                'type': 'exam',
                'date': conflict['exam_date'],
                'period': conflict['exam_period'],
                'count': conflict['count'],
                'details': conflict['exam_names']
            })
        
        return conflicts