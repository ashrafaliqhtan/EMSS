from django.db import models
from django.db import models
from django.contrib.auth.models import User
#from .models import Hall, Lecturer  # assuming Lecturer and Hall are defined
from django.db.models import Q
from django.db.models import Min, Max
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from django.db.models import Max
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class Lecturer(models.Model):

    LEVEL = (
        ('Assisstant', 'Assisstant Lecturers'),
        ('Lecturer 1', 'Lecturer 1'),
        ('Lecturer 2', 'Lecturer 2'),
        ('Lecturer 3', 'Lecturer 3'),
        ('Senior', 'Senior Lecturer'),
        ('Principal', 'Principal Lecturer'),
        ('Chief', 'Chief Lecturer'),
        ('HOD', 'Head of Department')
    )

    EXAM_TYPE = (
        ('CBE', 'Computer Based Exam'),
        ('PBE', 'Written Exam')
    )
    INVIGILATION_TYPE = (
        ('SUPERVISOR', 'Supervisor'),
        ('INVIGILATOR', 'Invigilator')
    )

    lecturer_name = models.CharField(max_length=50)
    lecturer_code = models.CharField(max_length=10)
    lecturer_level = models.CharField(max_length=50, choices=LEVEL)
    invigilation_type = models.CharField(
        max_length=20, choices=INVIGILATION_TYPE)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE)
    
    def get_conflicts(self):
        """الحصول على جميع التعارضات للمحاضر"""
        conflicts = []
        
        # تعارضات في جدول الامتحانات
        exam_conflicts = Exam.objects.filter(
            (Q(invigilator1=self) | Q(invigilator2=self)),
            exam_date__gte=date.today()
        ).values('exam_date', 'exam_period').annotate(
            count=Count('id'),
            exam_names=ArrayAgg('exam_name', distinct=True)
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
    
    def get_schedule(self):
        """الحصول على جدول المحاضر"""
        exams = Exam.objects.filter(
            (Q(invigilator1=self) | Q(invigilator2=self)),
            exam_date__gte=date.today()
        ).order_by('exam_date', 'exam_period')
        
        assignments = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=self) | Q(second_supervisor=self)),
            exam_date__gte=date.today()
        ).order_by('exam_date', 'exam_period')
        
        return {
            'exams': exams,
            'assignments': assignments
        }
    def get_schedule_conflicts(self):
        """الحصول على جميع التعارضات للمحاضر"""
        conflicts = []
        
        # تعارضات في جدول الامتحانات
        exam_assignments = ExamHallAssignment.objects.filter(
            models.Q(first_supervisor=self) | models.Q(second_supervisor=self)
        ).values('exam_date', 'exam_period').annotate(count=Count('id')).filter(count__gt=1)
        
        for assignment in exam_assignments:
            conflicts.append({
                'type': 'EXAM',
                'date': assignment['exam_date'],
                'period': assignment['exam_period'],
                'count': assignment['count']
            })
        
        return conflicts
    class META:
        ordering = ['lecturer_code']

    def __str__(self):
        return self.lecturer_name


# To create Examnation Hall Model
class Hall(models.Model):

    HALL_TYPES = (
        ('SM', 'Small'),
        ('MD', 'Medium'),
        ('LG', 'Large')
    )
    hall_name = models.CharField(max_length=50)
    hall_capacity = models.IntegerField()
    hall_type = models.CharField(max_length=50, choices=HALL_TYPES)
    def get_conflicts(self):
        """الحصول على تعارضات القاعة"""
        assignments = ExamHallAssignment.objects.filter(
            room_nos__contains=self.hall_name
        )
        
        conflicts = []
        for assignment in assignments:
            overlapping = ExamHallAssignment.objects.filter(
                room_nos__contains=self.hall_name,
                exam_date=assignment.exam_date,
                exam_period=assignment.exam_period
            ).exclude(id=assignment.id)
            
            if overlapping.exists():
                conflicts.append({
                    'date': assignment.exam_date,
                    'period': assignment.exam_period,
                    'assignments': [assignment] + list(overlapping)
                })
        
        return conflicts

    class META:
        ordering = ['hall_name']

    def __str__(self):
        return self.hall_name


# To create Block Model
class Block(models.Model):
    name = models.CharField(max_length=50)
    halls = models.ManyToManyField(Hall)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name


# To create Invigilator Schedule Model
class Invigilators(models.Model):

    PERIOD = (
        ('AM', 'Morning'),
        ('PM', 'Afternoon')
    )

    EXAM_TYPE = (
        ('CBE', 'Computer Based Exam'),
        ('PBE', 'Paper Based Exam')
    )

    lecture_code = models.CharField(max_length=5)
    exam_hall = models.CharField(max_length=50)
    courses = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=5, choices=EXAM_TYPE)
    exam_date = models.CharField(max_length=20)
    exam_period = models.CharField(max_length=5, choices=PERIOD)

    class META:
        ordering = ['exam_period']

    def __str__(self):
        return self.lecture_code


# To create supervisors Schedule Model
class Supervisors(models.Model):

    PERIOD = (
        ('AM', 'Morning'),
        ('PM', 'Afternoon')
    )

    EXAM_TYPE = (
        ('CBE', 'Computer Based Exam'),
        ('PBE', 'Paper Based Exam')
    )

    lecture_code = models.CharField(max_length=5)
    exam_block = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=5, choices=EXAM_TYPE)
    exam_date = models.CharField(max_length=20)
    exam_period = models.CharField(max_length=5, choices=PERIOD)

    class META:
        ordering = ['exam_period']

    def __str__(self):
        return self.lecture_code

  # assuming Hall is already defined





from django.core.exceptions import ValidationError

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

class Exam(models.Model):
    exam_name = models.CharField(max_length=200)
    exam_date = models.DateField()
    exam_hall = models.ForeignKey('Hall', on_delete=models.CASCADE)
    exam_type = models.CharField(
        max_length=50,
        choices=[('PBE', 'PBE'), ('CBE', 'CBE')]
    )
    exam_period = models.CharField(max_length=50)
    invigilator1 = models.ForeignKey(
        'Lecturer',
        related_name="exam_invigilator1",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    invigilator2 = models.ForeignKey(
        'Lecturer',
        related_name="exam_invigilator2",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def check_lecturer_conflicts(self, lecturer, exam_date, exam_period):
        """
        Check if lecturer has any conflicts during the specified exam period
        """
        # Check if lecturer is marked as unavailable
        if hasattr(lecturer, 'conflict_set'):
            if lecturer.conflict_set.filter(
                Q(created_at__date=exam_date) |  # Using created_at as proxy if conflict_date doesn't exist
                Q(exam_assignment__exam_date=exam_date, exam_assignment__exam_period=exam_period),
                resolved=False
            ).exists():
                raise ValidationError(
                    f"Lecturer {lecturer.name} has a conflict during {exam_period} on {exam_date}"
                )
        
        # Check if lecturer is already assigned to another exam at same time
        conflicting_exams = Exam.objects.filter(
            Q(invigilator1=lecturer) | Q(invigilator2=lecturer),
            exam_date=exam_date,
            exam_period=exam_period
        ).exclude(pk=self.pk)  # Exclude current exam when updating
        
        if conflicting_exams.exists():
            raise ValidationError(
                f"Lecturer {lecturer.name} is already assigned to another exam "
                f"during {exam_period} on {exam_date}"
            )

    def check_hall_conflicts(self, hall_name, exam_date, exam_period):
        """
        Check if hall is already booked for another exam during this period
        """
        conflicting_exams = Exam.objects.filter(
            exam_hall__hall_name=hall_name,
            exam_date=exam_date,
            exam_period=exam_period
        ).exclude(pk=self.pk)  # Exclude current exam when updating
        
        if conflicting_exams.exists():
            raise ValidationError(
                f"Hall {hall_name} is already booked for another exam "
                f"during {exam_period} on {exam_date}"
            )

    def clean(self):
        super().clean()
        
        # Check lecturer conflicts
        if self.invigilator1 and self.exam_date and self.exam_period:
            self.check_lecturer_conflicts(self.invigilator1, self.exam_date, self.exam_period)
        
        if self.invigilator2 and self.exam_date and self.exam_period:
            self.check_lecturer_conflicts(self.invigilator2, self.exam_date, self.exam_period)
        
        # Check hall conflicts (fixed typo in exam_period)
        if self.exam_hall and self.exam_date and self.exam_period:
            self.check_hall_conflicts(self.exam_hall.hall_name, self.exam_date, self.exam_period)
        
        # Check if same lecturer is assigned as both invigilators
        if self.invigilator1 and self.invigilator2 and self.invigilator1 == self.invigilator2:
            raise ValidationError("The same lecturer cannot be assigned as both invigilators")

    def __str__(self):
        return self.exam_name






class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invigilation_notifs',  # اسم فريد
        related_query_name='invigilation_notifs'  # اسم فريد للاستعلامات
    )
    # باقي الحقول...
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)
    @classmethod
    def unread_count(cls, user):
        return cls.objects.filter(user=user, read=False).count()

    def __str__(self):
        return self.message[:50]






# ------------------------------------------------------------------------------
# Exam Supervisor Model
# ------------------------------------------------------------------------------
class ExamSupervisor(models.Model):
    department = models.CharField(max_length=255, help_text="Department (DEPT)")
    academic_degree = models.CharField(max_length=100, help_text="Academic Degree")
    name = models.CharField(max_length=255, help_text="Supervisor Name")
    def get_conflicts(self):
        """الحصول على جميع التعارضات للمراقب"""
        conflicts = []
        
        # تعارضات في تخصيص القاعات
        assignment_conflicts = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=self) | Q(second_supervisor=self)),
            exam_date__gte=date.today()
        ).values('exam_date', 'exam_period').annotate(
            count=Count('id'),
            courses=ArrayAgg('course_code', distinct=True)
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
    
    def get_schedule(self):
        """الحصول على جدول المراقب"""
        return ExamHallAssignment.objects.filter(
            (Q(first_supervisor=self) | Q(second_supervisor=self)),
            exam_date__gte=date.today()
        ).order_by('exam_date', 'exam_period')

    def __str__(self):
        return self.name

# ------------------------------------------------------------------------------
# Exam Hall Assignment Model
# ------------------------------------------------------------------------------


"""
class ExamHallAssignment(models.Model):
    level = models.CharField(max_length=10, help_text="Example: 4")
    course_code = models.CharField(max_length=20, help_text="Example: COMP 213")
    course_name = models.CharField(max_length=255, help_text="Example: Programming - 29")
    section = models.CharField(max_length=10, blank=True, null=True, help_text="Section (if applicable)")
    total_students = models.PositiveIntegerField(help_text="Total number of students")
    students_per_room = models.PositiveIntegerField(help_text="Number of students per room")
    from_to = models.CharField(max_length=50, help_text="From-To range (e.g., 18-19)")
    room_nos = models.CharField(max_length=255, help_text="Room numbers (comma separated, e.g., F12,F13)")

    # Two supervisors can be assigned to the exam hall.
    first_supervisor = models.ForeignKey(
        ExamSupervisor,
        related_name='first_supervisor_halls',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select the first supervisor"
    )
    second_supervisor = models.ForeignKey(
        ExamSupervisor,
        related_name='second_supervisor_halls',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select the second supervisor"
    )

    # Timestamp fields for record tracking.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        section_str = f" (Section: {self.section})" if self.section else ""
        return f"{self.course_code} - {self.course_name}{section_str}"
"""


class ExamHallAssignment(models.Model):
    PERIOD_CHOICES = [
        ('AM', 'Morning'),
        ('PM', 'Afternoon'),
    ]
    
    level = models.CharField(max_length=10, help_text="Example: 4")
    course_code = models.CharField(max_length=20, help_text="Example: COMP 213")
    course_name = models.CharField(max_length=255, help_text="Example: Programming - 29")
    section = models.CharField(max_length=10, blank=True, null=True, help_text="Section (if applicable)")
    total_students = models.PositiveIntegerField(help_text="Total number of students")
    students_per_room = models.PositiveIntegerField(help_text="Number of students per room")
    from_to = models.CharField(max_length=50, help_text="From-To range (e.g., 18-19)")
    room_nos = models.CharField(max_length=255, help_text="Room numbers (comma separated, e.g., F12,F13)")
    
    # Exam date and period fields for conflict detection
    exam_date = models.DateField(help_text="Date of the exam", null=True, blank=True)
    exam_period = models.CharField(
        max_length=2,
        choices=PERIOD_CHOICES,
        help_text="Exam period (Morning/Afternoon)",
        null=True,
        blank=True
    )

    # Two supervisors can be assigned to the exam hall.
    first_supervisor = models.ForeignKey(
        ExamSupervisor,
        related_name='first_supervisor_halls',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select the first supervisor"
    )
    second_supervisor = models.ForeignKey(
        ExamSupervisor,
        related_name='second_supervisor_halls',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select the second supervisor"
    )

    # Timestamp fields for record tracking.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_supervisor', 'exam_date', 'exam_period'],
                name='unique_first_supervisor_schedule'
            ),
            models.UniqueConstraint(
                fields=['second_supervisor', 'exam_date', 'exam_period'],
                name='unique_second_supervisor_schedule'
            ),
        ]
        ordering = ['exam_date', 'exam_period', 'course_code']

    def __str__(self):
        section_str = f" (Section: {self.section})" if self.section else ""
        return f"{self.course_code} - {self.course_name}{section_str}"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        super().clean()
        
        # Check if both date and period are provided
        if not self.exam_date or not self.exam_period:
            raise ValidationError("Exam date and period are required for conflict checking")
        
        # Check first supervisor conflicts
        if self.first_supervisor:
            conflicts = ExamHallAssignment.objects.filter(
                models.Q(first_supervisor=self.first_supervisor) |
                models.Q(second_supervisor=self.first_supervisor),
                exam_date=self.exam_date,
                exam_period=self.exam_period
            ).exclude(pk=self.pk)
            
            if conflicts.exists():
                raise ValidationError(
                    f"{self.first_supervisor.name} is already assigned to another "
                    f"hall on {self.exam_date} ({self.get_exam_period_display()})"
                )
        
        # Check second supervisor conflicts
        if self.second_supervisor:
            conflicts = ExamHallAssignment.objects.filter(
                models.Q(first_supervisor=self.second_supervisor) |
                models.Q(second_supervisor=self.second_supervisor),
                exam_date=self.exam_date,
                exam_period=self.exam_period
            ).exclude(pk=self.pk)
            
            if conflicts.exists():
                raise ValidationError(
                    f"{self.second_supervisor.name} is already assigned to another "
                    f"hall on {self.exam_date} ({self.get_exam_period_display()})"
                )
        
        # Check if first and second supervisors are the same
        if (self.first_supervisor and self.second_supervisor and 
            self.first_supervisor == self.second_supervisor):
            raise ValidationError(
                "First and second supervisors cannot be the same person"
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation runs on save
        super().save(*args, **kwargs)
        
        
        














class ConflictCheckMixin:
    def check_lecturer_conflicts(self, lecturer, exam_date, exam_period):
        """تحقق من تعارضات المحاضر/المراقب"""
        # تعارضات في جدول الامتحانات
        exam_conflicts = Exam.objects.filter(
            (Q(invigilator1=lecturer) | Q(invigilator2=lecturer)),
            exam_date=exam_date,
            exam_period=exam_period
        ).exclude(id=self.id if hasattr(self, 'id') else None)
        
        if exam_conflicts.exists():
            conflict_details = ", ".join([e.exam_name for e in exam_conflicts[:3]])
            if exam_conflicts.count() > 3:
                conflict_details += f" و{exam_conflicts.count()-3} أخرى"
            
            self.create_conflict_record(
                'LECTURER',
                f"المحاضر {lecturer.lecturer_name} لديه تعيين في امتحان آخر ({conflict_details}) في نفس التوقيت",
                lecturer
            )
            raise ValidationError(
                _("المحاضر %(name)s لديه تعيين في امتحان آخر (%(exams)s) في نفس التوقيت"),
                params={'name': lecturer.lecturer_name, 'exams': conflict_details},
            )

    def check_hall_conflicts(self, hall_name, exam_date, exam_period):
        """تحقق من تعارضات القاعة"""
        # تعارضات في جدول الامتحانات
        exam_conflicts = Exam.objects.filter(
            exam_hall__hall_name=hall_name,
            exam_date=exam_date,
            exam_period=exam_period
        ).exclude(id=self.id if hasattr(self, 'id') else None)
        
        if exam_conflicts.exists():
            conflict_details = ", ".join([e.exam_name for e in exam_conflicts[:3]])
            if exam_conflicts.count() > 3:
                conflict_details += f" و{exam_conflicts.count()-3} أخرى"
            
            self.create_conflict_record(
                'HALL',
                f"القاعة {hall_name} محجوزة لامتحان آخر ({conflict_details}) في نفس التوقيت",
                exam_conflicts.first().exam_hall
            )
            raise ValidationError(
                _("القاعة %(hall)s محجوزة لامتحان آخر (%(exams)s) في نفس التوقيت"),
                params={'hall': hall_name, 'exams': conflict_details},
            )

    def check_supervisor_conflicts(self, supervisor, exam_date, exam_period):
        """تحقق من تعارضات المراقب"""
        # تعارضات في تخصيص القاعات
        assignment_conflicts = ExamHallAssignment.objects.filter(
            (Q(first_supervisor=supervisor) | Q(second_supervisor=supervisor)),
            exam_date=exam_date,
            exam_period=exam_period
        ).exclude(id=self.id if hasattr(self, 'id') else None)
        
        if assignment_conflicts.exists():
            conflict_details = ", ".join([a.course_code for a in assignment_conflicts[:3]])
            if assignment_conflicts.count() > 3:
                conflict_details += f" و{assignment_conflicts.count()-3} أخرى"
            
            self.create_conflict_record(
                'SUPERVISOR',
                f"المراقب {supervisor.name} لديه تعيين في قاعة أخرى ({conflict_details}) في نفس التوقيت",
                supervisor
            )
            raise ValidationError(
                _("المراقب %(name)s لديه تعيين في قاعة أخرى (%(courses)s) في نفس التوقيت"),
                params={'name': supervisor.name, 'courses': conflict_details},
            )

    def create_conflict_record(self, conflict_type, description, obj):
        """إنشاء سجل تعارض في قاعدة البيانات"""
        Conflict.objects.create(
            conflict_type=conflict_type,
            description=description,
            related_object_id=obj.id,
            related_object_type=obj.__class__.__name__
        )
    


class Conflict1(models.Model):
    RESOLVED_CHOICES = (
        (False, 'غير محلول'),
        (True, 'محلول')
    )
    
    lecturer = models.ForeignKey(Lecturer, null=True, blank=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(ExamSupervisor, null=True, blank=True, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, null=True, blank=True, on_delete=models.CASCADE)
    exam_assignment = models.ForeignKey(ExamHallAssignment, on_delete=models.CASCADE)
    conflict_type = models.CharField(max_length=20)
    description = models.TextField()
    resolved = models.BooleanField(choices=RESOLVED_CHOICES, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_conflict_type_display()} - {self.description[:50]}"



class Conflict(models.Model):
    RESOLVED_CHOICES = (
        (False, 'غير محلول'),
        (True, 'محلول')
    )
    CONFLICT_TYPES = (
        ('LECTURER', 'تعارض محاضر'),
        ('HALL', 'تعارض قاعة'),
        ('TIMING', 'تعارض توقيت'),
        ('SUPERVISOR', 'تعارض مراقب'),
    )
    lecturer = models.ForeignKey(Lecturer, null=True, blank=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(ExamSupervisor, null=True, blank=True, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, null=True, blank=True, on_delete=models.CASCADE)
    exam_assignment = models.ForeignKey(ExamHallAssignment, on_delete=models.CASCADE)
    conflict_type = models.CharField(max_length=20, choices=CONFLICT_TYPES)
    description = models.TextField()
    related_object_id = models.PositiveIntegerField()
    related_object_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'تعارض'
        verbose_name_plural = 'تعارضات'
    
    def __str__(self):
        return f"{self.get_conflict_type_display()} - {self.description[:50]}"