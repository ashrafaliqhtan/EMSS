from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.apps import apps
from django.utils import timezone
from .models import (
    Lecturer, Hall, Invigilators, Supervisors, Block,
    Conflict, Exam, ExamHallAssignment, ExamSupervisor
)

class ConflictAdmin(admin.ModelAdmin):
    list_display = ('conflict_type', 'short_description', 'related_object_link', 
                   'resolved', 'created_at', 'resolution_actions')
    list_filter = ('conflict_type', 'resolved', 'created_at')
    search_fields = ('description', 'related_object_type')
    list_editable = ('resolved',)
    actions = ['mark_as_resolved']
    readonly_fields = ('created_at', 'resolved_at')
    fieldsets = (
        (None, {
            'fields': ('conflict_type', 'description', 'resolved')
        }),
        ('تفاصيل التعارض', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('حل التعارض', {
            'fields': ('resolved_by', 'resolved_at', 'resolution_notes'),
            'classes': ('collapse',)
        }),
    )

    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    short_description.short_description = 'الوصف'
    
    def related_object_link(self, obj):
        try:
            model = apps.get_model('invigilation', obj.related_object_type)
            related_obj = model.objects.get(pk=obj.related_object_id)
            url = reverse(f'admin:invigilation_{obj.related_object_type.lower()}_change', args=[related_obj.id])
            return format_html('<a href="{}">{}</a>', url, str(related_obj))
        except:
            return "غير متاح"
    related_object_link.short_description = 'الكائن المتعلق'
    
    def resolution_actions(self, obj):
        if not obj.resolved:
            return format_html(
                '<a class="button" href="{}">حل التعارض</a>',
                reverse('admin:invigilation_conflict_resolve', args=[obj.id])
            )
        return "تم الحل"
    resolution_actions.short_description = 'إجراءات'
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(
            resolved=True, 
            resolved_by=request.user, 
            resolved_at=timezone.now()
        )
        self.message_user(request, f"تم تحديد {updated} تعارضات كمحلولة")
    mark_as_resolved.short_description = "حل التعارضات المحددة"

class LecturerAdmin(admin.ModelAdmin):
    list_display = ('lecturer_name', 'lecturer_code', 'lecturer_level', 
                   'invigilation_type', 'exam_type', 'conflict_count')
    list_filter = ('lecturer_level', 'invigilation_type', 'exam_type')
    search_fields = ('lecturer_name', 'lecturer_code')

    def conflict_count(self, obj):
        count = Conflict.objects.filter(
            related_object_type='Lecturer',
            related_object_id=obj.id,
            resolved=False
        ).count()
        if count > 0:
            return format_html('<span style="color: red;">{}</span>', count)
        return count
    conflict_count.short_description = 'التعارضات'

class HallAdmin(admin.ModelAdmin):
    list_display = ('hall_name', 'hall_capacity', 'hall_type', 'blocks_list')
    list_filter = ('hall_type',)
    
    def blocks_list(self, obj):
        return ", ".join([block.name for block in obj.block_set.all()])
    blocks_list.short_description = 'المباني'

class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date', 'exam_period', 
                   'exam_hall', 'invigilators', 'conflict_status')
    list_filter = ('exam_type', 'exam_period', 'exam_date')
    search_fields = ('exam_name', 'exam_hall__hall_name')
    raw_id_fields = ('invigilator1', 'invigilator2')
    date_hierarchy = 'exam_date'

    def invigilators(self, obj):
        return f"{obj.invigilator1 or '--'} / {obj.invigilator2 or '--'}"
    invigilators.short_description = 'المراقبون'
    
    def conflict_status(self, obj):
        conflicts = Conflict.objects.filter(
            related_object_type='Exam',
            related_object_id=obj.id,
            resolved=False
        ).count()
        if conflicts > 0:
            return format_html(
                '<a href="{}?resolved__exact=0&related_object_type__exact=Exam&related_object_id__exact={}" style="color: red;">{} تعارضات</a>',
                reverse('admin:invigilation_conflict_changelist'),
                obj.id,
                conflicts
            )
        return "بدون تعارضات"
    conflict_status.short_description = 'حالة التعارض'

class ExamHallAssignmentAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'exam_date', 
                   'exam_period', 'room_nos', 'supervisors', 'conflict_status')
    list_filter = ('exam_period', 'exam_date', 'level')
    search_fields = ('course_code', 'course_name', 'room_nos')
    raw_id_fields = ('first_supervisor', 'second_supervisor')
    date_hierarchy = 'exam_date'

    def supervisors(self, obj):
        return f"{obj.first_supervisor or '--'} / {obj.second_supervisor or '--'}"
    supervisors.short_description = 'المراقبون'
    
    def conflict_status(self, obj):
        conflicts = Conflict.objects.filter(
            related_object_type='ExamHallAssignment',
            related_object_id=obj.id,
            resolved=False
        ).count()
        if conflicts > 0:
            return format_html(
                '<a href="{}?resolved__exact=0&related_object_type__exact=ExamHallAssignment&related_object_id__exact={}" style="color: red;">{} تعارضات</a>',
                reverse('admin:invigilation_conflict_changelist'),
                obj.id,
                conflicts
            )
        return "بدون تعارضات"
    conflict_status.short_description = 'حالة التعارض'

class ExamSupervisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'academic_degree', 'assignment_count', 'conflict_count')
    list_filter = ('department',)
    search_fields = ('name', 'department')
    
    def assignment_count(self, obj):
        return obj.first_supervisor_halls.count() + obj.second_supervisor_halls.count()
    assignment_count.short_description = 'عدد التكليفات'
    
    def conflict_count(self, obj):
        count = Conflict.objects.filter(
            related_object_type='ExamSupervisor',
            related_object_id=obj.id,
            resolved=False
        ).count()
        if count > 0:
            return format_html('<span style="color: red;">{}</span>', count)
        return count
    conflict_count.short_description = 'التعارضات'

class InvigilatorsAdmin(admin.ModelAdmin):
    list_display = ('lecture_code', 'exam_hall', 'courses', 'exam_date', 'exam_period')
    list_filter = ('exam_period', 'exam_type')
    search_fields = ('lecture_code', 'exam_hall', 'courses')
    # تم إزالة date_hierarchy لأن exam_date ليس DateField

class SupervisorsAdmin(admin.ModelAdmin):
    list_display = ('lecture_code', 'exam_block', 'exam_date', 'exam_period')
    list_filter = ('exam_period', 'exam_type')
    search_fields = ('lecture_code', 'exam_block')
    # تم إزالة date_hierarchy لأن exam_date ليس DateField

class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'halls_count')
    
    def halls_count(self, obj):
        return obj.halls.count()
    halls_count.short_description = 'عدد القاعات'

# تسجيل النماذج
admin.site.register(Conflict, ConflictAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamHallAssignment, ExamHallAssignmentAdmin)
admin.site.register(ExamSupervisor, ExamSupervisorAdmin)
admin.site.register(Invigilators, InvigilatorsAdmin)
admin.site.register(Supervisors, SupervisorsAdmin)
admin.site.register(Block, BlockAdmin)

# إعدادات عامة لوحة الإدارة
admin.site.site_header = "نظام إدارة الامتحانات"
admin.site.site_title = "نظام إدارة الامتحانات"
admin.site.index_title = "مرحبا بكم في لوحة التحكم"