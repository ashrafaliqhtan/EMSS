from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Lecturer, ExamSupervisor, Hall, ExamHallAssignment

@login_required
def conflict_dashboard(request):
    # إحصائيات التعارضات
    lecturers_with_conflicts = Lecturer.objects.annotate(
        conflict_count=Count('examhallassignment_first_supervisor', 
                           filter=~Q(examhallassignment_first_supervisor__resolved=True))
    ).filter(conflict_count__gt=0)
    
    halls_with_conflicts = Hall.objects.annotate(
        conflict_count=Count('examhallassignment', 
                           filter=~Q(examhallassignment__resolved=True))
    ).filter(conflict_count__gt=0)
    
    context = {
        'lecturers_with_conflicts': lecturers_with_conflicts,
        'halls_with_conflicts': halls_with_conflicts,
    }
    return render(request, 'conflicts/dashboard.html', context)

@login_required
def resolve_conflict(request, pk):
    conflict = get_object_or_404(Conflict, pk=pk)
    if request.method == 'POST':
        conflict.resolved = True
        conflict.resolved_by = request.user
        conflict.save()
        return redirect('conflict_dashboard')
    return render(request, 'conflicts/resolve.html', {'conflict': conflict})

@login_required
def lecturer_conflicts_report(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
    conflicts = lecturer.get_conflicts()
    return render(request, 'conflicts/lecturer_report.html', {
        'lecturer': lecturer,
        'conflicts': conflicts
    })

@login_required
def supervisor_conflicts_report(request, supervisor_id):
    supervisor = get_object_or_404(ExamSupervisor, pk=supervisor_id)
    conflicts = supervisor.get_conflicts()
    return render(request, 'conflicts/supervisor_report.html', {
        'supervisor': supervisor,
        'conflicts': conflicts
    })

@login_required
def hall_conflicts_report(request, hall_id):
    hall = get_object_or_404(Hall, pk=hall_id)
    conflicts = hall.get_conflicts()
    return render(request, 'conflicts/hall_report.html', {
        'hall': hall,
        'conflicts': conflicts
    })