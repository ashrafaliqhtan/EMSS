# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Exam, ExamHallAssignment, Conflict

@receiver(pre_save, sender=Exam)
def check_exam_conflicts(sender, instance, **kwargs):
    instance.full_clean()  # سيؤدي إلى تنفيذ التحقق من التعارضات

@receiver(pre_save, sender=ExamHallAssignment)
def check_assignment_conflicts(sender, instance, **kwargs):
    instance.full_clean()  # سيؤدي إلى تنفيذ التحقق من التعارضات

@receiver(post_save, sender=Conflict)
def notify_about_conflict(sender, instance, created, **kwargs):
    if created and not instance.resolved:
        # إرسال إشعار للمسؤولين عن التعارض الجديد
        from django.contrib.auth.models import User
        from notifications.models import Notification
        
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"تعارض جديد: {instance.description}",
                link=f"/admin/exam/conflict/{instance.id}/change/"
            )