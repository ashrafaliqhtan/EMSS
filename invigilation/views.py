from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django import forms
import pandas as pd
import random
from typing import List
from django.contrib.auth.models import User
from notifications.views import send_notification
from .models import Exam
from .forms import ExamForm  # if you moved ExamForm to forms.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Hall, Lecturer, Invigilators, Supervisors, Block
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Exam
from .forms import ExamForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from django.db.models import Max
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ExamSupervisor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ExamHallAssignment
from .forms import ExamHallAssignmentForm
from django.db.models import Min, Max
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from django.db.models import Max
from datetime import date
from django.db.models import Q
from datetime import timedelta, datetime
from django.db.models import Count, Q
from .models import ExamHallAssignment, ExamSupervisor

from .models import Lecturer, ExamHallAssignment, ExamSupervisor
from .forms import (  # Add this import
    LecturerForm,
    ExamHallAssignmentForm,
    ExamSupervisorForm
)
import pandas as pd
from .utils import ConflictUtils

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
# views/conflicts.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Case, When, IntegerField, Q
# أضف في الأعلى:

from django.db.models import Q, Count
from django.db import models  # Add this import


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Lecturer, Exam, ExamHallAssignment
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import csv
from openpyxl import Workbook
from io import BytesIO

def export_exams(request):
    export_format = request.GET.get('format', 'pdf')
    exams = Exam.objects.all().order_by('exam_date', 'exam_period')
    
    if export_format == 'pdf':
        # PDF Export
        html_string = render_to_string('invigilation/export_exams_pdf.html', {'exams': exams})
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="exams_export.pdf"'
        return response
      
    elif export_format == 'csv':
        # CSV Export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exams_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Exam Name', 'Date', 'Hall', 'Type', 'Period', 'Invigilator 1', 'Invigilator 2'])
        
        for exam in exams:
            writer.writerow([
                exam.exam_name,
                exam.exam_date,
                exam.exam_hall.hall_name,
                exam.exam_type,
                exam.exam_period,
                exam.invigilator1.lecturer_name if exam.invigilator1 else '',
                exam.invigilator2.lecturer_name if exam.invigilator2 else ''
            ])
            
        return response
        
    elif export_format == 'excel':
        # Excel Export
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="exams_export.xlsx"'
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Exams"
        
        # Add headers
        ws.append(['Exam Name', 'Date', 'Hall', 'Type', 'Period', 'Invigilator 1', 'Invigilator 2'])
        
        # Add data
        for exam in exams:
            ws.append([
                exam.exam_name,
                exam.exam_date,
                exam.exam_hall.hall_name,
                exam.exam_type,
                exam.exam_period,
                exam.invigilator1.lecturer_name if exam.invigilator1 else '',
                exam.invigilator2.lecturer_name if exam.invigilator2 else ''
            ])
        
        # Save to response
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        response.write(output.read())
        
        return response
        
    return HttpResponse("Invalid export format", status=400)

from django.db import IntegrityError
from datetime import date, timedelta
import random
from django.contrib import messages
from django.shortcuts import redirect, render

@login_required

def generate_schedule(request):
    if request.method == 'POST':
        try:
            # Clear existing assignments
            Exam.objects.all().update(invigilator1=None, invigilator2=None)
            
            # Get date range
            today = date.today()
            end_date = today + timedelta(days=30)
            
            # Get all exams with optimized queries
            exams = Exam.objects.filter(
                exam_date__gte=today,
                exam_date__lte=end_date
            ).select_related('exam_hall', 'invigilator1', 'invigilator2').order_by('exam_date', 'exam_period')
            
            # Group exams by date and period
            exam_groups = {}
            for exam in exams:
                key = (exam.exam_date, exam.exam_period)
                exam_groups.setdefault(key, []).append(exam)
            
            # Pre-fetch all lecturers by exam type
            lecturer_cache = {}  # {exam_type: [lecturers]}
            
            for (exam_date, exam_period), exam_list in exam_groups.items():
                exam_type = exam_list[0].exam_type
                
                # Cache lecturers by exam type
                if exam_type not in lecturer_cache:
                    lecturer_cache[exam_type] = list(Lecturer.objects.filter(exam_type=exam_type))
                
                lecturers = lecturer_cache[exam_type].copy()
                random.shuffle(lecturers)
                
                for exam in exam_list:
                    assigned = 0
                    temp_lecturers = lecturers.copy()
                    
                    while assigned < 2 and temp_lecturers:
                        lecturer = temp_lecturers.pop()
                        if not Conflict.objects.filter(
                            lecturer=lecturer,
                            conflict_date=exam_date,
                            conflict_period=exam_period
                        ).exists():
                            if assigned == 0:
                                exam.invigilator1 = lecturer
                            else:
                                exam.invigilator2 = lecturer
                            assigned += 1
                            lecturers.remove(lecturer)
                    
                    exam.save()
            
            messages.success(request, f"Schedule generated for {len(exams)} exams!")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('dashboard')
    
    # GET request handling
    today = date.today()
    end_date = today + timedelta(days=30)
    exam_count = Exam.objects.filter(
        exam_date__gte=today,
        exam_date__lte=end_date
    ).count()
    
    return render(request, 'invigilation/generate_schedule.html', {
        'exam_count': exam_count,
        'date_range': f"{today.strftime('%b %d')} to {end_date.strftime('%b %d')}"
    })


@login_required
def lecturer_conflicts(request, lecturer_id):
    """تفاصيل تعارضات محاضر معين"""
    lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
    
    # Get exam conflicts (only checking Exams where lecturer is invigilator)
    exam_conflicts = Exam.objects.filter(
        (Q(invigilator1=lecturer) | Q(invigilator2=lecturer)),
        exam_date__gte=date.today()
    ).values('exam_date', 'exam_period').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    # Get conflicts from ExamHallAssignment (only if lecturer is also an ExamSupervisor)
    assignment_conflicts = []
    if hasattr(lecturer, 'examsupervisor'):
        supervisor = lecturer.examsupervisor
        assignment_conflicts = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor)),
            exam_date__gte=date.today()
        ).values('exam_date', 'exam_period').annotate(
            count=Count('id')
        ).filter(count__gt=1)
    
    # Build combined conflicts list
    conflicts = []
    for conflict in exam_conflicts:
        exams = Exam.objects.filter(
            exam_date=conflict['exam_date'],
            exam_period=conflict['exam_period'],
            invigilator1=lecturer
        )
        conflicts.append({
            'type': 'exam',
            'date': conflict['exam_date'],
            'period': conflict['exam_period'],
            'count': conflict['count'],
            'details': [e.exam_name for e in exams]
        })
    
    for conflict in assignment_conflicts:
        assignments = ExamHallAssignment.objects.filter(
            exam_date=conflict['exam_date'],
            exam_period=conflict['exam_period'],
            first_supervisor=lecturer.examsupervisor
        )
        conflicts.append({
            'type': 'assignment',
            'date': conflict['exam_date'],
            'period': conflict['exam_period'],
            'count': conflict['count'],
            'details': [f"{a.course_code} - {a.course_name}" for a in assignments]
        })
    
    # Get schedule
    exams = Exam.objects.filter(
        (Q(invigilator1=lecturer) | Q(invigilator2=lecturer)),
        exam_date__gte=date.today()
    ).order_by('exam_date', 'exam_period')
    
    assignments = []
    if hasattr(lecturer, 'examsupervisor'):
        assignments = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=lecturer.examsupervisor) | Q(second_supervisor=lecturer.examsupervisor)),
            exam_date__gte=date.today()
        ).order_by('exam_date', 'exam_period')
    
    context = {
        'lecturer': lecturer,
        'conflicts': conflicts,
        'schedule': {
            'exams': exams,
            'assignments': assignments
        }
    }
    return render(request, 'conflicts/lecturer_details.html', context)




@login_required
def supervisor_conflicts(request, supervisor_id):
    """تفاصيل تعارضات مراقب معين"""
    supervisor = get_object_or_404(ExamSupervisor, pk=supervisor_id)
    
    # Get conflicts (alternative to ConflictUtils)
    conflicts = []
    assignments = ExamHallAssignment.objects.filter(
        Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor),
        exam_date__gte=date.today()
    ).order_by('exam_date', 'exam_period')
    
    for assignment in assignments:
        overlapping = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor)),
            exam_date=assignment.exam_date,
            exam_period=assignment.exam_period
        ).exclude(id=assignment.id)
        
        if overlapping.exists():
            conflicts.append({
                'assignment': assignment,
                'overlapping_assignments': overlapping
            })
    
    # Get schedule using model method
    schedule = supervisor.get_schedule()
    
    context = {
        'supervisor': supervisor,
        'conflicts': conflicts,
        'schedule': schedule
    }
    return render(request, 'conflicts/supervisor_details.html', context)
@login_required
def hall_conflicts(request, hall_id):
    """تفاصيل تعارضات قاعة معينة"""
    from ..models import Hall
    hall = Hall.objects.get(pk=hall_id)
    conflicts = ConflictUtils.get_hall_conflicts(hall)
    
    context = {
        'hall': hall,
        'conflicts': conflicts
    }
    return render(request, 'conflicts/hall_details.html', context)
    




@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(read=False).count()
    
    # تحديد الإشعارات غير المقروءة
    unread_notifications = notifications.filter(read=False)
    
    # تحديث حالة الإشعارات إلى مقروءة عند فتح القائمة
    unread_notifications.update(read=True)
    
    return render(request, 'invigilation/notifications_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
    
    
    
    



@login_required
def conflict_dashboard(request):
    # Unresolved conflicts
    unresolved_conflicts = Conflict.objects.filter(resolved=False).order_by('-created_at')
    
    # Conflict statistics
    conflict_stats = {
        'total': Conflict.objects.count(),
        'unresolved': unresolved_conflicts.count(),
        'by_type': Conflict.objects.values('conflict_type').annotate(count=Count('id'))
    }
    
    # Lecturer conflicts (using Exam model instead of ExamHallAssignment)
    lecturer_conflicts = Lecturer.objects.annotate(
        conflict_count=Count(
            'exam_invigilator1',
            filter=Q(exam_invigilator1__isnull=False)
        ) + Count(
            'exam_invigilator2',
            filter=Q(exam_invigilator2__isnull=False)
        )
    ).filter(conflict_count__gt=0).order_by('-conflict_count')[:10]
    
    # Supervisor conflicts (using ExamHallAssignment)
    supervisor_conflicts = ExamSupervisor.objects.annotate(
        conflict_count=Count(
            'first_supervisor_halls',
            filter=Q(first_supervisor_halls__isnull=False)
        ) + Count(
            'second_supervisor_halls',
            filter=Q(second_supervisor_halls__isnull=False)
        )
    ).filter(conflict_count__gt=0).order_by('-conflict_count')[:10]
    
    # Hall conflicts
    today = date.today()
    hall_conflicts = ExamHallAssignment.objects.filter(
        exam_date__gte=today
    ).values('room_nos').annotate(
        conflict_count=Count('id', filter=Q(conflict__resolved=False)),
        first_date=Min('exam_date'),
        last_date=Max('exam_date')
    ).filter(conflict_count__gt=1).order_by('-conflict_count')[:10]
    
    context = {
        'unresolved_conflicts': unresolved_conflicts[:10],
        'conflict_stats': conflict_stats,
        'lecturer_conflicts': lecturer_conflicts,
        'supervisor_conflicts': supervisor_conflicts,
        'hall_conflicts': hall_conflicts,
    }
    return render(request, 'conflicts/dashboard.html', context)

@login_required
def resolve_conflict(request, pk):
    conflict = get_object_or_404(Conflict, pk=pk)
    
    if request.method == "POST":
        resolution_notes = request.POST.get('resolution_notes', '')
        conflict.resolved = True
        conflict.resolution_notes = resolution_notes
        conflict.resolved_by = request.user
        conflict.resolved_at = timezone.now()
        conflict.save()
        
        messages.success(request, "تم حل التعارض بنجاح")
        return redirect('conflict_dashboard')
    
    # الحصول على الكائن المتعلق بالتعارض
    try:
        related_object = getattr(models, conflict.related_object_type).objects.get(
            pk=conflict.related_object_id
        )
    except:
        related_object = None
    
    return render(request, 'conflicts/resolve.html', {
        'conflict': conflict,
        'related_object': related_object
    })

@login_required
def lecturer_conflicts_report(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
    
    # تعارضات الجدولة
    schedule_conflicts = ExamHallAssignment.objects.filter(
        (Q(first_supervisor=lecturer) | Q(second_supervisor=lecturer)) &
        Q(conflict__resolved=False)
    ).distinct()
    
    # تعارضات التواريخ
    date_conflicts = ExamHallAssignment.objects.filter(
        (Q(first_supervisor=lecturer) | Q(second_supervisor=lecturer))
    ).values('exam_date', 'exam_period').annotate(
        count=Count('id'),
        assignments=ArrayAgg('id')
    ).filter(count__gt=1)
    
    context = {
        'lecturer': lecturer,
        'schedule_conflicts': schedule_conflicts,
        'date_conflicts': date_conflicts,
    }
    return render(request, 'conflicts/lecturer_report.html', context)    
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from .models import ExamSupervisor, ExamHallAssignment, Hall, Conflict

def supervisor_conflicts_report(request, supervisor_id):
    supervisor = get_object_or_404(ExamSupervisor, pk=supervisor_id)
    
    # تعارضات الجدولة للمراقب
    assignments = ExamHallAssignment.objects.filter(
        Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor)
    ).order_by('exam_date', 'exam_period')
    
    # اكتشاف التعارضات
    conflicts = []
    for assignment in assignments:
        overlapping = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor)),
            exam_date=assignment.exam_date,
            exam_period=assignment.exam_period
        ).exclude(id=assignment.id)
        
        if overlapping.exists():
            conflicts.append({
                'assignment': assignment,
                'overlapping_assignments': overlapping
            })
    
    context = {
        'supervisor': supervisor,
        'conflicts': conflicts,
        'total_conflicts': len(conflicts),
        'assignments': assignments
    }
    return render(request, 'conflicts/supervisor_report.html', context)

def hall_conflicts_report(request, hall_id):
    hall = get_object_or_404(Hall, pk=hall_id)
    
    # تعارضات الجدولة للقاعة
    assignments = ExamHallAssignment.objects.filter(
        room_nos__contains=hall.hall_name
    ).order_by('exam_date', 'exam_period')
    
    # اكتشاف التعارضات
    conflicts = []
    for assignment in assignments:
        overlapping = ExamHallAssignment.objects.filter(
            room_nos__contains=hall.hall_name,
            exam_date=assignment.exam_date,
            exam_period=assignment.exam_period
        ).exclude(id=assignment.id)
        
        if overlapping.exists():
            conflicts.append({
                'assignment': assignment,
                'overlapping_assignments': overlapping
            })
    
    context = {
        'hall': hall,
        'conflicts': conflicts,
        'total_conflicts': len(conflicts),
        'assignments': assignments
    }
    return render(request, 'conflicts/hall_report.html', context)

class ExamHallAssignmentForm(forms.ModelForm):
    class Meta:
        model = ExamHallAssignment
        fields = [
            'level', 
            'course_code', 
            'course_name',
            'section',
            'total_students',
            'students_per_room',
            'from_to',
            'room_nos',
            'first_supervisor',
            'second_supervisor',
            'exam_date',  # تأكد من وجود هذا الحقل في النموذج
            'exam_period'  # تأكد من وجود هذا الحقل في النموذج
        ]
        labels = {
            'level': 'Level',
            'course_code': 'Course Code',
            'course_name': 'Course Name',
            'section': 'Section',
            'total_students': 'Total Students',
            'students_per_room': 'Students per Room',
            'from_to': 'From-To',
            'room_nos': 'Room Nos.',
            'first_supervisor': 'First Supervisor',
            'second_supervisor': 'Second Supervisor',
            'exam_date': 'Exam Date',
            'exam_period': 'Exam Period'
        }

    def clean(self):
        cleaned_data = super().clean()
        first_supervisor = cleaned_data.get('first_supervisor')
        second_supervisor = cleaned_data.get('second_supervisor')
        exam_date = cleaned_data.get('exam_date')
        exam_period = cleaned_data.get('exam_period')

        # تحقق من تعارضات المراقب الأول
        if first_supervisor and exam_date and exam_period:
            conflicting_assignments = ExamHallAssignment.objects.filter(
                models.Q(first_supervisor=first_supervisor) | 
                models.Q(second_supervisor=first_supervisor),
                exam_date=exam_date,
                exam_period=exam_period
            ).exclude(id=self.instance.id if self.instance else None)
            
            if conflicting_assignments.exists():
                self.add_error('first_supervisor', 
                             "هذا المراقب موجود بالفعل في قاعة أخرى في نفس التاريخ والفترة")

        # تحقق من تعارضات المراقب الثاني
        if second_supervisor and exam_date and exam_period:
            conflicting_assignments = ExamHallAssignment.objects.filter(
                models.Q(first_supervisor=second_supervisor) | 
                models.Q(second_supervisor=second_supervisor),
                exam_date=exam_date,
                exam_period=exam_period
            ).exclude(id=self.instance.id if self.instance else None)
            
            if conflicting_assignments.exists():
                self.add_error('second_supervisor', 
                             "هذا المراقب موجود بالفعل في قاعة أخرى في نفس التاريخ والفترة")

        # تحقق من عدم تعيين نفس الشخص كمراقب أول وثاني
        if first_supervisor and second_supervisor and first_supervisor == second_supervisor:
            self.add_error('second_supervisor', 
                         "لا يمكن أن يكون المراقب الأول والثاني نفس الشخص")

        return cleaned_data



@login_required(login_url='login')




@login_required
def exam_hall_panel(request):
    # معالجة معاملات البحث والتصفية
    search_query = request.GET.get('search', '')
    date_filter = request.GET.get('date', '')
    period_filter = request.GET.get('period', '')
    supervisor_filter = request.GET.get('supervisor', '')
    level_filter = request.GET.get('level', '')

    # استعلام أساسي
    exam_halls = ExamHallAssignment.objects.all().order_by('exam_date', 'exam_period', 'course_code')

    # تطبيق الفلاتر
    if search_query:
        exam_halls = exam_halls.filter(
            Q(course_code__icontains=search_query) |
            Q(course_name__icontains=search_query) |
            Q(room_nos__icontains=search_query)
        )

    if date_filter:
        exam_halls = exam_halls.filter(exam_date=date_filter)

    if period_filter:
        exam_halls = exam_halls.filter(exam_period=period_filter)

    if supervisor_filter:
        exam_halls = exam_halls.filter(
            Q(first_supervisor__id=supervisor_filter) |
            Q(second_supervisor__id=supervisor_filter)
        )

    if level_filter:
        exam_halls = exam_halls.filter(level=level_filter)

    # حساب الحد الأقصى لعدد الطلاب لتحديد النسبة المئوية
    max_students = exam_halls.aggregate(max_students=Max('total_students'))['max_students'] or 1

    # التقسيم إلى صفحات
    paginator = Paginator(exam_halls, 15)  # 15 عنصر لكل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # إحصائيات
    total_assignments = exam_halls.count()
    today_assignments = exam_halls.filter(exam_date=date.today()).count()
    upcoming_assignments = exam_halls.filter(exam_date__gt=date.today()).count()
    no_supervisors_count = exam_halls.filter(first_supervisor__isnull=True, second_supervisor__isnull=True).count()

    # الحصول على جميع المراقبين والمستويات للفلترة
    all_supervisors = ExamSupervisor.objects.all().order_by('name')
    all_levels = ExamHallAssignment.objects.values_list('level', flat=True).distinct().order_by('level')

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'date_filter': date_filter,
        'period_filter': period_filter,
        'supervisor_filter': supervisor_filter,
        'level_filter': level_filter,
        'total_assignments': total_assignments,
        'today_assignments': today_assignments,
        'upcoming_assignments': upcoming_assignments,
        'no_supervisors_count': no_supervisors_count,
        'current_date': date.today().isoformat(),
        'max_students': max_students,
        'all_supervisors': all_supervisors,
        'all_levels': all_levels,
        'exam_halls': exam_halls  # Added this line to include the queryset in context
    }
    return render(request, 'invigilation/exam_hall_panel.html', context)

@login_required(login_url='login')
def create_exam_hall(request):
    if request.method == "POST":
        form = ExamHallAssignmentForm(request.POST)
        if form.is_valid():
            try:
                exam_assignment = form.save(commit=False)
                exam_assignment.full_clean()  # تنفيذ التحقق الإضافي
                exam_assignment.save()
                messages.success(request, "تم إنشاء تخصيص قاعة الامتحان بنجاح.")
                return redirect('exam_hall_panel')
            except Exception as e:
                messages.error(request, f"خطأ في إنشاء تخصيص القاعة: {str(e)}")
        else:
            # عرض أخطاء النموذج للمستخدم
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ExamHallAssignmentForm()
    
    return render(request, 'invigilation/create_exam_hall.html', {
        'form': form,
        'form_title': 'إنشاء تخصيص قاعة امتحان جديد'
    })

@login_required(login_url='login')
def edit_exam_hall(request, pk):
    exam_hall = get_object_or_404(ExamHallAssignment, pk=pk)
    if request.method == "POST":
        form = ExamHallAssignmentForm(request.POST, instance=exam_hall)
        if form.is_valid():
            try:
                exam_assignment = form.save(commit=False)
                exam_assignment.full_clean()  # تنفيذ التحقق الإضافي
                exam_assignment.save()
                messages.success(request, "تم تحديث تخصيص قاعة الامتحان بنجاح.")
                return redirect('exam_hall_panel')
            except Exception as e:
                messages.error(request, f"خطأ في تحديث تخصيص القاعة: {str(e)}")
        else:
            # عرض أخطاء النموذج للمستخدم
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ExamHallAssignmentForm(instance=exam_hall)
    
    return render(request, 'invigilation/edit_exam_hall.html', {
        'form': form,
        'form_title': 'تعديل تخصيص قاعة الامتحان'
    })

@login_required(login_url='login')
def delete_exam_hall(request, pk):
    exam_hall = get_object_or_404(ExamHallAssignment, pk=pk)
    if request.method == "POST":
        try:
            exam_hall.delete()
            messages.success(request, "تم حذف تخصيص قاعة الامتحان بنجاح.")
            return redirect('exam_hall_panel')
        except Exception as e:
            messages.error(request, f"خطأ في حذف تخصيص القاعة: {str(e)}")
            return redirect('exam_hall_panel')
    
    return render(request, 'invigilation/confirm_delete_exam_hall.html', {
        'exam_hall': exam_hall
    })
# 
@login_required(login_url='login')
# 
@login_required(login_url='login')
def delete_all_exam_halls(request):
    if request.method == "POST":
        ExamHallAssignment.objects.all().delete()
        messages.success(request, "All exam hall assignments have been deleted.")
        return redirect('exam_hall_panel')
    return render(request, 'invigilation/confirm_delete_all_exam_halls.html')

# 
@login_required(login_url='login')
def upload_exam_halls(request):
    if request.method == "POST" and request.FILES.get('exam_halls'):
        try:
            df = pd.read_csv(request.FILES['exam_halls'])
            # Loop through each row and create an ExamHallAssignment.
            for _, row in df.iterrows():
                # Attempt to get the first and second supervisors by name.
                first_sup = None
                second_sup = None
                if 'first_supervisor' in row and pd.notna(row['first_supervisor']):
                    try:
                        first_sup = ExamSupervisor.objects.get(name=row['first_supervisor'])
                    except ExamSupervisor.DoesNotExist:
                        first_sup = None
                if 'second_supervisor' in row and pd.notna(row['second_supervisor']):
                    try:
                        second_sup = ExamSupervisor.objects.get(name=row['second_supervisor'])
                    except ExamSupervisor.DoesNotExist:
                        second_sup = None

                ExamHallAssignment.objects.create(
                    level=row['level'],
                    course_code=row['course_code'],
                    course_name=row['course_name'],
                    section=row.get('section', None),
                    total_students=int(row['total_students']),
                    students_per_room=int(row['students_per_room']),
                    from_to=row['from_to'],
                    room_nos=row['room_nos'],
                    first_supervisor=first_sup,
                    second_supervisor=second_sup,
                )
            messages.success(request, "Exam hall assignments uploaded successfully.")
        except Exception as e:
            messages.error(request, f"Error uploading exam hall assignments: {str(e)}")
        return redirect('exam_hall_panel')
    return redirect('exam_hall_panel')




class ExamSupervisorForm(forms.ModelForm):
    class Meta:

        model = ExamSupervisor
        fields = ['department', 'academic_degree', 'name']
        labels = {
            'department': 'DEPT',
            'academic_degree': 'Academic Degree',
            'name': 'NAME',
        }


@login_required(login_url='login')
def exam_supervisor_panel(request):
    exam_supervisors = ExamSupervisor.objects.all().order_by('id')  # id acts as SI
    return render(request, 'invigilation/exam_supervisor_panel.html', {
        'exam_supervisors': exam_supervisors
    })

# Create a new Exam Supervisor
@login_required(login_url='login')
def create_exam_supervisor(request):
    if request.method == "POST":
        form = ExamSupervisorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam Supervisor created successfully.")
            return redirect('exam_supervisor_panel')
    else:
        form = ExamSupervisorForm()
    return render(request, 'invigilation/create_exam_supervisor.html', {
        'form': form
    })

# Edit an existing Exam Supervisor
@login_required(login_url='login')
def edit_exam_supervisor(request, pk):
    exam_supervisor = get_object_or_404(ExamSupervisor, pk=pk)
    if request.method == "POST":
        form = ExamSupervisorForm(request.POST, instance=exam_supervisor)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam Supervisor updated successfully.")
            return redirect('exam_supervisor_panel')
    else:
        form = ExamSupervisorForm(instance=exam_supervisor)
    return render(request, 'invigilation/edit_exam_supervisor.html', {
        'form': form
    })

# Delete a single Exam Supervisor (confirmation page)
@login_required(login_url='login')
def delete_exam_supervisor(request, pk):
    exam_supervisor = get_object_or_404(ExamSupervisor, pk=pk)
    if request.method == "POST":
        exam_supervisor.delete()
        messages.success(request, "Exam Supervisor deleted successfully.")
        return redirect('exam_supervisor_panel')
    return render(request, 'invigilation/confirm_delete_exam_supervisor.html', {
        'exam_supervisor': exam_supervisor
    })

# Delete all Exam Supervisors (bulk delete with confirmation)
@login_required(login_url='login')
def delete_all_exam_supervisors(request):
    if request.method == "POST":
        ExamSupervisor.objects.all().delete()
        messages.success(request, "All exam supervisors have been deleted.")
        return redirect('exam_supervisor_panel')
    return render(request, 'invigilation/confirm_delete_all_exam_supervisors.html')

# 
@login_required(login_url='login')
def upload_exam_supervisors(request):
    if request.method == "POST" and request.FILES.get('exam_supervisors'):
        try:
            df = pd.read_csv(request.FILES['exam_supervisors'])
            for _, row in df.iterrows():

                ExamSupervisor.objects.update_or_create(
                    id=row.get('SI'), 

                    defaults={
                        'department': row['DEPT'],
                        'academic_degree': row['Academic Degree'],
                        'name': row['NAME']
                    }
                )
            messages.success(request, "Exam Supervisors uploaded successfully.")
        except Exception as e:
            messages.error(request, f"Error uploading exam supervisors: {str(e)}")
        return redirect('exam_supervisor_panel')
    return redirect('exam_supervisor_panel')




class InvigilatorForm(forms.ModelForm):
    exam_hall = forms.ModelChoiceField(queryset=Hall.objects.all(), to_field_name='hall_name')

    class Meta:
        model = Invigilators
        fields = ['lecture_code', 'exam_hall', 'courses', 'exam_type', 'exam_date', 'exam_period']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exam_hall'].label_from_instance = lambda obj: obj.hall_name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.exam_hall = self.cleaned_data['exam_hall'].hall_name
        if commit:
            instance.save()
        return instance


class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisors
        fields = ['lecture_code', 'exam_block', 'exam_date', 'exam_type', 'exam_period']


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['hall_name', 'hall_capacity', 'hall_type']



def userlogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'invigilation/login.html')


def userlogout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
    
    return render(request, 'invigilation/signup.html')





@login_required(login_url='login')
def exam_list(request):
    query = request.GET.get('q', '')
    if query:
        exams = Exam.objects.filter(exam_name__icontains=query)
    else:
        exams = Exam.objects.all()
    return render(request, 'invigilation/exam_list.html', {'exams': exams, 'query': query})

@login_required(login_url='login')
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'invigilation/exam_detail.html', {'exam': exam})


"""def create_exam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam created successfully")
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'invigilation/create_exam.html', {'form': form})"""






# views.py


@login_required(login_url='login')
def create_exam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            # Save exam and get instance
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            
            # Send real-time notifications to all users
            users = User.objects.all()
            message = f"New exam scheduled: {exam.exam_name}"
            exam_url = reverse('exam_detail', kwargs={'pk': exam.pk})
            
            # Get channel layer
            channel_layer = get_channel_layer()
            
            # Send bulk notifications
            async_to_sync(channel_layer.group_send)(
                "bulk_notifications",
                {
                    "type": "send.bulk_notifications",
                    "users": [user.id for user in users],
                    "message": {
                        "type": "exam_created",
                        "message": message,
                        "exam_id": exam.id,
                        "link": exam_url,
                        "timestamp": str(timezone.now()),
                        "created_by": request.user.username
                    }
                }
            )

            messages.success(request, "Exam created successfully!")
            return redirect('exam_list')
        
        # If form is invalid
        messages.error(request, "Error creating exam. Please check the form.")
        return render(request, 'invigilation/create_exam.html', {'form': form})

    # GET request - show empty form
    form = ExamForm()
    context = {
        'form': form,
        'page_title': 'Create New Exam',
        'submit_label': 'Create Exam'
    }
    return render(request, 'invigilation/create_exam.html', context)
    
    
@login_required(login_url='login')
def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated successfully")
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'invigilation/edit_exam.html', {'form': form})

@login_required(login_url='login')
def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        exam.delete()
        messages.success(request, "Exam deleted successfully")
        return redirect('exam_list')
    return render(request, 'invigilation/confirm_delete_exam.html', {'exam': exam})

@login_required(login_url='login')
def upload_exams(request):
    if request.method == "POST" and request.FILES.get('exams_csv'):
        try:
            df = pd.read_csv(request.FILES['exams_csv'])

            for _, row in df.iterrows():
                hall = Hall.objects.get(hall_name=row['exam_hall'])
                inv1 = Lecturer.objects.get(lecturer_code=row['invigilator1']) if pd.notna(row.get('invigilator1')) else None
                inv2 = Lecturer.objects.get(lecturer_code=row['invigilator2']) if pd.notna(row.get('invigilator2')) else None
                Exam.objects.create(
                    exam_name=row['exam_name'],
                    exam_date=row['exam_date'],
                    exam_hall=hall,
                    exam_type=row['exam_type'],
                    exam_period=row['exam_period'],
                    invigilator1=inv1,
                    invigilator2=inv2
                )
            messages.success(request, "Exams uploaded successfully")
        except Exception as e:
            messages.error(request, f"Error uploading exams: {str(e)}")
        return redirect('exam_list')
    return render(request, 'invigilation/upload_exams.html')

    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        exam.delete()
        messages.success(request, "Exam deleted successfully")
        return redirect('exam_list')
    return render(request, 'invigilation/confirm_delete_exam.html', {'exam': exam})




def homePage(request):
    return render(request, 'invigilation/home.html')

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from .models import Exam, Hall, Lecturer, Block, Conflict, ExamHallAssignment
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Exam, Hall, Lecturer, Conflict, Block, ExamHallAssignment
@login_required(login_url='login')












def dashboard(request):
    today = timezone.now().date()
    
    # Date range filter
    date_range = request.GET.get('range', 'week')
    exam_type_filter = request.GET.get('exam_type', 'all')
    hall_filter = request.GET.get('hall', 'all')
    period_filter = request.GET.get('period', 'all')

    # Base queryset with select_related for performance
    exams = Exam.objects.select_related('exam_hall', 'invigilator1', 'invigilator2')
    upcoming_exams = exams.filter(exam_date__gte=today)
    
    # Apply filters
    if date_range == 'today':
        upcoming_exams = upcoming_exams.filter(exam_date=today)
    elif date_range == 'week':
        upcoming_exams = upcoming_exams.filter(
            exam_date__range=[today, today + timedelta(days=7)])
    elif date_range == 'month':
        upcoming_exams = upcoming_exams.filter(
            exam_date__range=[today, today + timedelta(days=30)])
    
    if exam_type_filter != 'all':
        upcoming_exams = upcoming_exams.filter(exam_type=exam_type_filter)
    
    if hall_filter != 'all':
        upcoming_exams = upcoming_exams.filter(exam_hall__hall_name=hall_filter)
    
    if period_filter != 'all':
        upcoming_exams = upcoming_exams.filter(exam_period=period_filter)

    # Statistics calculations
    current_week_count = exams.filter(
        exam_date__range=[today, today + timedelta(days=7)]
    ).count()

    # Utilization Calculations
    # Hall Utilization
    halls_in_use = Hall.objects.annotate(exam_count=Count('exam')).filter(exam_count__gt=0)
    total_halls = Hall.objects.count()
    hall_utilization_percent = round((halls_in_use.count() / total_halls) * 100) if total_halls > 0 else 0
    hall_usage_details = ExamHallAssignment.objects.values('room_nos').annotate(
        exam_count=Count('id')
    ).order_by('-exam_count')[:5]

    # Lecturer Utilization
    assigned_lecturers = Lecturer.objects.filter(
        Q(exam_invigilator1__isnull=False) | 
        Q(exam_invigilator2__isnull=False)
    ).distinct().count()
    total_lecturers = Lecturer.objects.count()
    lecturer_utilization = round((assigned_lecturers / total_lecturers) * 100) if total_lecturers > 0 else 0

    # Conflict Resolution
    resolved_conflicts = Conflict.objects.filter(resolved=True).count()
    total_conflicts = Conflict.objects.count()
    conflict_resolution_rate = round((resolved_conflicts / total_conflicts) * 100) if total_conflicts > 0 else 0

    # Conflict Analysis
    conflict_types = Conflict.objects.values_list('conflict_type', flat=True).distinct()
    conflicts_by_type = []
    
    for conflict_type in conflict_types:
        total = Conflict.objects.filter(conflict_type=conflict_type).count()
        resolved = Conflict.objects.filter(conflict_type=conflict_type, resolved=True).count()
        conflicts_by_type.append({
            'conflict_type': conflict_type,
            'count': total,
            'resolved': resolved,
            'unresolved': total - resolved,
            'resolution_rate': round((resolved / total) * 100) if total > 0 else 0
        })

    context = {
        # Basic stats
        "total_halls": total_halls,
        "total_lecturers": total_lecturers,
        "total_blocks": Block.objects.count(),
        
        # Exam stats
        "exam_count": current_week_count,
        "upcoming_exams": upcoming_exams.order_by('exam_date', 'exam_period'),
        "total_upcoming_exams": upcoming_exams.count(),
        "today": today,
        
        # Filters
        "date_range": date_range,
        "exam_type_filter": exam_type_filter,
        "hall_filter": hall_filter,
        "period_filter": period_filter,
        "all_halls": Hall.objects.all(),
        
        # Conflict data
        "active_conflicts": Conflict.objects.filter(resolved=False).count(),
        "conflicts_by_type": conflicts_by_type,
        
        # Utilization metrics
        "hall_utilization_percent": hall_utilization_percent,
        "hall_usage_details": hall_usage_details,
        "used_halls": halls_in_use.count(),
        "lecturer_utilization": lecturer_utilization,
        "assigned_lecturers": assigned_lecturers,
        "conflict_resolution_rate": conflict_resolution_rate,
        "resolved_conflicts": resolved_conflicts,
        "total_conflicts": total_conflicts,
        "last_updated": timezone.now(),
    }
    
    return render(request, 'invigilation/dashboard.html', context)

def get_conflict_trend_data():
    # Generate last 7 days conflict trend data
    dates = []
    resolved_counts = []
    unresolved_counts = []
    
    for i in range(7):
        date = timezone.now().date() - timedelta(days=(6-i))
        dates.append(date.strftime('%a'))
        resolved_counts.append(
            Conflict.objects.filter(
                created_at__date=date,
                resolved=True
            ).count()
        )
        unresolved_counts.append(
            Conflict.objects.filter(
                created_at__date=date,
                resolved=False
            ).count()
        )
    
    return {
        'dates': dates,
        'resolved': resolved_counts,
        'unresolved': unresolved_counts
    }



@login_required(login_url='login')
def dashboard1(request):
    stats = {
        "total_halls": Hall.objects.count(),
        "total_lecturers": Lecturer.objects.count(),
        "total_blocks": Block.objects.count(),
        "pbe_lecturers": Lecturer.objects.filter(exam_type="PBE").count(),
        "cbe_lecturers": Lecturer.objects.filter(exam_type="CBE").count(),
        "pbe_invigilators": Lecturer.objects.filter(exam_type="PBE", invigilation_type="INVIGILATOR").count(),
        "pbe_supervisors": Lecturer.objects.filter(exam_type="PBE", invigilation_type="SUPERVISOR").count(),
        "cbe_invigilators": Lecturer.objects.filter(exam_type="CBE", invigilation_type="INVIGILATOR").count(),
        "cbe_supervisors": Lecturer.objects.filter(exam_type="CBE", invigilation_type="SUPERVISOR").count(),
    }
    return render(request, 'invigilation/dashboard1.html', stats)




@login_required(login_url='login')
def halls(request):
    hall_list = Hall.objects.prefetch_related('block_set').all()  # Get all halls and their blocks

    halls = [
        {
            "id": hall.id,
            "block": ", ".join(block.name for block in hall.block_set.all()),  # Join multiple blocks
            "name": hall.hall_name,
            "capacity": hall.hall_capacity,
            "type": hall.get_hall_type_display(),
        }
        for hall in hall_list
    ]

    return render(request, 'invigilation/halls.html', {"halls": halls})  # Ensure context name matches template




@login_required(login_url='login')
def lecturers(request):
    return render(request, 'invigilation/lecturers.html', {
        "lecturers": Lecturer.objects.all()
    })



class Schedule:
    def __init__(self, courses, block, exam_hall, exam_day, hall_type, exam_type, exam_period):
        self.courses = courses
        self.block = block
        self.exam_hall = exam_hall
        self.exam_day = exam_day
        self.hall_type = hall_type
        self.exam_type = exam_type
        self.exam_period = exam_period


class LecturerQueue:
    def __init__(self, lecturers):
        self.lecturers = lecturers.copy()
        self.pointer = 0

    def next(self):
        if self.pointer >= len(self.lecturers):
            self.pointer = 0
        lecturer = self.lecturers[self.pointer]
        self.pointer += 1
        return lecturer


def is_conflict(lecturer_code, exam_day, exam_period):
    return Invigilators.objects.filter(
        lecture_code=lecturer_code,
        exam_date=exam_day,
        exam_period=exam_period
    ).exists()


def schedule_invigilators(schedules, lecturer_queue, schedule_list):
    for schedule in schedules:
        lecturers_needed = min(len(schedule.courses.split(',')), 6)
        assigned = []
        attempts = 0
        
        while len(assigned) < lecturers_needed and attempts < len(lecturer_queue.lecturers):
            lecturer = lecturer_queue.next()
            if not is_conflict(lecturer['lecturer_code'], schedule.exam_day, schedule.exam_period):
                assigned.append(lecturer)
            attempts += 1
        
        if assigned:
            schedule_list.append({
                "schedule": schedule,
                "lecturers": assigned
            })



@login_required(login_url='login')
def schedule(request):
    if request.method == "POST" and request.FILES.get('courses'):
        try:
            # Process CSV data
            df = pd.read_csv(request.FILES['courses'])
            schedules = [
                Schedule(
                    courses=row['courses'],
                    block=row['block'],
                    exam_hall=row['exam_hall'],
                    exam_day=row['exam_date'],
                    hall_type=row['hall_type'],
                    exam_type=row['exam_type'],
                    exam_period=row['exam_period']
                )
                for _, row in df.iterrows()
            ]

            # Prepare lecturer queues
            lecturers = list(Lecturer.objects.values())
            pbe_invig = LecturerQueue([lec for lec in lecturers if lec['exam_type'] == 'PBE' and lec['invigilation_type'] == 'INVIGILATOR'])
            cbe_invig = LecturerQueue([lec for lec in lecturers if lec['exam_type'] == 'CBE' and lec['invigilation_type'] == 'INVIGILATOR'])
            pbe_super = LecturerQueue([lec for lec in lecturers if lec['exam_type'] == 'PBE' and lec['invigilation_type'] == 'SUPERVISOR'])
            cbe_super = LecturerQueue([lec for lec in lecturers if lec['exam_type'] == 'CBE' and lec['invigilation_type'] == 'SUPERVISOR'])

            # Schedule invigilators and supervisors
            invigilator_schedules = []
            supervisor_schedules = []
            
            # Schedule invigilators
            for date in df['exam_date'].unique():
                pbe_schedules = [s for s in schedules if s.exam_day == date and s.exam_type == 'PBE']
                cbe_schedules = [s for s in schedules if s.exam_day == date and s.exam_type == 'CBE']
                schedule_invigilators(pbe_schedules, pbe_invig, invigilator_schedules)
                schedule_invigilators(cbe_schedules, cbe_invig, invigilator_schedules)

            # Schedule supervisors
            for block in df['block'].unique():
                block_schedules = [s for s in schedules if s.block == block]
                for sched in block_schedules:
                    sups = []
                    for _ in range(2):  # Assign 2 supervisors
                        sup = pbe_super.next() if sched.exam_type == 'PBE' else cbe_super.next()
                        sups.append(sup)
                    supervisor_schedules.append({
                        "schedule": sched,
                        "lecturers": sups
                    })

            # Save to database
            Invigilators.objects.all().delete()
            for item in invigilator_schedules:
                for lec in item['lecturers']:
                    Invigilators.objects.create(
                        lecture_code=lec['lecturer_code'],
                        exam_hall=item['schedule'].exam_hall,
                        courses=item['schedule'].courses,
                        exam_type=item['schedule'].exam_type,
                        exam_date=item['schedule'].exam_day,
                        exam_period=item['schedule'].exam_period
                    )

            Supervisors.objects.all().delete()
            for item in supervisor_schedules:
                for lec in item['lecturers']:
                    Supervisors.objects.create(
                        lecture_code=lec['lecturer_code'],
                        exam_block=item['schedule'].block,
                        exam_type=item['schedule'].exam_type,
                        exam_date=item['schedule'].exam_day,
                        exam_period=item['schedule'].exam_period
                    )

            messages.success(request, 'Schedule generated successfully')
            return redirect('schedule')

        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
    
    return render(request, 'invigilation/schedule.html', {
        "invigilators": Invigilators.objects.all(),
        "supervisors": Supervisors.objects.all()
    })



@login_required(login_url='login')
def upload_hall(request):
    if request.method == "POST" and request.FILES.get('halls'):
        try:
            df = pd.read_csv(request.FILES['halls'])
            for _, row in df.iterrows():
                hall, _ = Hall.objects.update_or_create(
                    hall_name=row['LECTURE ROOM'],
                    defaults={
                        'hall_capacity': row['CAPACITY'],
                        'hall_type': row['TYPE']
                    }
                )
                block, _ = Block.objects.get_or_create(name=row['LECTURE BLOCK'])
                block.halls.add(hall)
            messages.success(request, 'Halls uploaded successfully')
        except Exception as e:
            messages.error(request, f'Error uploading halls: {str(e)}')
        return redirect('halls')
    return redirect('halls')


@login_required(login_url='login')
def upload_lecturers(request):
    if request.method == "POST" and request.FILES.get('lecturers'):
        try:
            df = pd.read_csv(request.FILES['lecturers'])
            for _, row in df.iterrows():
                Lecturer.objects.update_or_create(
                    lecturer_code=row['Lecturer Code'],
                    defaults={
                        'lecturer_name': row['Lecturer Name'],
                        'lecturer_level': row['Lecturer Status'],
                        'invigilation_type': row['Invigilation Type'],
                        'exam_type': row['Exam Type']
                    }
                )
            messages.success(request, 'Lecturers uploaded successfully')
        except Exception as e:
            messages.error(request, f'Error uploading lecturers: {str(e)}')
        return redirect('lecturers')
    return redirect('lecturers')



@login_required(login_url='login')
def edit_invigilator(request, pk):
    invigilator = get_object_or_404(Invigilators, pk=pk)
    if request.method == "POST":
        form = InvigilatorForm(request.POST, instance=invigilator)
        if form.is_valid():
            form.save()
            messages.success(request, "Invigilator updated")
            return redirect('schedule')
    else:
        form = InvigilatorForm(instance=invigilator)
    return render(request, 'invigilation/edit_invigilator.html', {'form': form})


@login_required(login_url='login')
def create_invigilator(request):
    if request.method == "POST":
        form = InvigilatorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Invigilator created")
            return redirect('schedule')
    else:
        form = InvigilatorForm()
    return render(request, 'invigilation/create_invigilator.html', {'form': form})


@login_required(login_url='login')
def edit_supervisor(request, pk):
    supervisor = get_object_or_404(Supervisors, pk=pk)
    if request.method == "POST":
        form = SupervisorForm(request.POST, instance=supervisor)
        if form.is_valid():
            form.save()
            messages.success(request, "Supervisor updated")
            return redirect('schedule')
    else:
        form = SupervisorForm(instance=supervisor)
    return render(request, 'invigilation/edit_supervisor.html', {'form': form})


@login_required(login_url='login')
def create_supervisor(request):
    if request.method == "POST":
        form = SupervisorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supervisor created")
            return redirect('schedule')
    else:
        form = SupervisorForm()
    return render(request, 'invigilation/create_supervisor.html', {'form': form})


@login_required(login_url='login')
def edit_hall(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    if request.method == "POST":
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            messages.success(request, "Hall updated")
            return redirect('halls')
    else:
        form = HallForm(instance=hall)
    return render(request, 'invigilation/edit_hall.html', {'form': form})


@login_required(login_url='login')
def create_hall(request):
    if request.method == "POST":
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hall created")
            return redirect('halls')
    else:
        form = HallForm()
    return render(request, 'invigilation/create_hall.html', {'form': form})





# Create a Lecturer
@login_required(login_url='login')
def create_lecturer(request):
    if request.method == "POST":
        form = LecturerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecturer created")
            return redirect('lecturers')
    else:
        form = LecturerForm()
    return render(request, 'invigilation/create_lecturer.html', {'form': form})


# Edit a Lecturer
@login_required(login_url='login')
def edit_lecturer(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    if request.method == "POST":
        form = LecturerForm(request.POST, instance=lecturer)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecturer updated")
            return redirect('lecturers')
    else:
        form = LecturerForm(instance=lecturer)
    return render(request, 'invigilation/edit_lecturer.html', {'form': form})


# Delete a single Lecturer
@login_required(login_url='login')
def delete_lecturer(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    if request.method == "POST":
        lecturer.delete()
        messages.success(request, f"Lecturer {lecturer.lecturer_name} was deleted successfully")
        return redirect('lecturers')
    
    # If not POST, show confirmation page (for non-JS users)
    return render(request, 'invigilation/confirm_delete_lecturer.html', {'lecturer': lecturer})


# Delete all Lecturers (with confirmation)
@login_required(login_url='login')
def delete_all_lecturers(request):
    if request.method == "POST":
        Lecturer.objects.all().delete()
        messages.success(request, "All lecturers deleted")
        return redirect('lecturers')
    return render(request, 'invigilation/confirm_delete_all_lecturers.html')


@user_passes_test(lambda u: u.groups.filter(name='Committee').exists(), login_url='login')
def committee_dashboard(request):
    return render(request, 'invigilation/committee_dashboard.html', {
        "invigilators": Invigilators.objects.all(),
        "supervisors": Supervisors.objects.all()
    })


# views.py


# views.py
import json
from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import make_naive
from datetime import datetime
import json
from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import make_naive, is_aware
from datetime import datetime
from .models import Exam, Lecturer
from django.shortcuts import render
@login_required(login_url='login')








def reports_backend(request):
    # Aggregate exam data with proper date ordering
    exam_report = (
        Exam.objects
        .values('exam_date')
        .annotate(count=Count('id'))
        .order_by('exam_date')
    )
    
    # Prepare chart data - ensure dates are in correct format
    exam_dates = []
    exam_counts = []
    
    for item in exam_report:
        if item['exam_date']:
            exam_dates.append(item['exam_date'].isoformat())  # YYYY-MM-DD format
            exam_counts.append(item['count'])
    
    # Prepare lecturer data with percentages
    lecturer_report = list(
        Lecturer.objects
        .values('invigilation_type')
        .annotate(count=Count('id'))
        .order_by('invigilation_type')
    )
    
    total_lecturers = sum(item['count'] for item in lecturer_report) if lecturer_report else 0
    
    # Add percentages to lecturer data
    lecturer_report_with_percent = []
    for item in lecturer_report:
        percent = (item['count'] / total_lecturers * 100) if total_lecturers > 0 else 0
        lecturer_report_with_percent.append({
            **item,
            'percentage': round(percent, 2)
        })
    
    context = {
        'exam_report': exam_report,
        'lecturer_report': lecturer_report_with_percent,
        'exam_dates': json.dumps(exam_dates),
        'exam_counts': json.dumps(exam_counts),
        'total_exams': sum(exam_counts) if exam_counts else 0,
        'total_lecturers': total_lecturers,
        'exam_periods': len(exam_dates),
    }
    return render(request, 'reports/reports_backend.html', context)

@login_required(login_url='login')
def reports_frontend(request):
    """
    Frontend reports view for regular users.
    Provides summary statistics.
    """
    exam_count = Exam.objects.count()
    lecturer_count = Lecturer.objects.count()
    hall_count = Hall.objects.count()
    
    context = {
        'exam_count': exam_count,
        'lecturer_count': lecturer_count,
        'hall_count': hall_count,
    }
    return render(request, 'reports/reports_frontend.html', context)

@login_required(login_url='login')
def reports_frontend(request):
    """
    Frontend reports view for regular users.
    Provides summary statistics.
    """
    exam_count = Exam.objects.count()
    lecturer_count = Lecturer.objects.count()
    hall_count = Hall.objects.count()
    
    context = {
        'exam_count': exam_count,
        'lecturer_count': lecturer_count,
        'hall_count': hall_count,
    }
    return render(request, 'reports/reports_frontend.html', context)








