class ExamSupervisor(models.Model):
    # الحقول الحالية...
    
    def get_conflicts(self):
        """الحصول على تعارضات المراقب"""
        assignments = ExamHallAssignment.objects.filter(
            Q(first_supervisor=self) | Q(second_supervisor=self)
        )
        
        conflicts = []
        for assignment in assignments:
            overlapping = ExamHallAssignment.objects.filter(
                (Q(first_supervisor=self) | Q(second_supervisor=self)),
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

class Hall(models.Model):
    # الحقول الحالية...
    
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