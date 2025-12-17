from django import forms
from .models import Exam
# forms.py (KEEP ONLY FORMS)
from django import forms
from .models import Lecturer, ExamHallAssignment, ExamSupervisor  # Import models from models.py

# Add this missing form definition
from django import forms
from django.db import models
from .models import Exam, Lecturer, ExamHallAssignment, ExamSupervisor



class ExamForm(forms.ModelForm):
    exam_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Exam
        fields = [
            'exam_name',
            'exam_date',
            'exam_hall',
            'exam_type',
            'exam_period',
            'invigilator1',
            'invigilator2'
        ]
        labels = {
            'exam_name': 'Exam Name',
            'exam_hall': 'Exam Hall',
            'exam_type': 'Exam Type',
            'exam_period': 'Exam Period'
        }
# models.py



class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = '__all__'



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
from django import forms
from .models import ExamSupervisor, Hall

class SupervisorReportForm(forms.Form):
    supervisor = forms.ModelChoiceField(
        queryset=ExamSupervisor.objects.all(),
        label="المراقب",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        label="من تاريخ",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    date_to = forms.DateField(
        label="إلى تاريخ",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

class HallReportForm(forms.Form):
    hall = forms.ModelChoiceField(
        queryset=Hall.objects.all(),
        label="القاعة",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        label="من تاريخ",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    date_to = forms.DateField(
        label="إلى تاريخ",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
class ExamSupervisorForm(forms.ModelForm):
    class Meta:
        model = ExamSupervisor
        fields = ['department', 'academic_degree', 'name']





def check_supervisor_conflict(supervisor, exam_date, exam_period):
    """تحقق مما إذا كان المراقب موجودًا بالفعل في قاعة أخرى في نفس التاريخ والفترة"""
    conflicting_assignments = ExamHallAssignment.objects.filter(
        models.Q(first_supervisor=supervisor) | models.Q(second_supervisor=supervisor),
        exam_date=exam_date,
        exam_period=exam_period
    )
    return conflicting_assignments.exists()