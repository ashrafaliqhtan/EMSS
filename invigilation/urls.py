from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import export_exams
urlpatterns = [
    # Authentication URLs
    path('', views.homePage, name='home'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('signup/', views.signup, name='signup'),
    
    
    
    # Scheduling
    
    path('generate-schedule/', views.generate_schedule, name='generate_schedule'),
    path('export-exams/', export_exams, name='export_exams'),
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard1/', views.dashboard1, name='dashboard1'),
    
    # Hall Management URLs
    path('halls/', views.halls, name='halls'),
    path('halls/create/', views.create_hall, name='create_hall'),
    path('halls/edit/<int:pk>/', views.edit_hall, name='edit_hall'),
    path('halls/upload/', views.upload_hall, name='upload_hall'),
    
    # Lecturer Management URLs
    path('lecturers/', views.lecturers, name='lecturers'),
    path('lecturers/create/', views.create_lecturer, name='create_lecturer'),
    path('lecturers/edit/<int:pk>/', views.edit_lecturer, name='edit_lecturer'),
    path('lecturers/delete/<int:pk>/', views.delete_lecturer, name='delete_lecturer'),
    path('lecturers/delete-all/', views.delete_all_lecturers, name='delete_all_lecturers'),
    path('lecturers/upload/', views.upload_lecturers, name='upload_lecturers'),
    
    # Exam Management URLs
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.create_exam, name='create_exam'),
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exams/edit/<int:pk>/', views.edit_exam, name='edit_exam'),
    path('exams/delete/<int:pk>/', views.delete_exam, name='delete_exam'),
    path('exams/upload/', views.upload_exams, name='upload_exams'),
    
    # Exam Hall Assignment URLs
    path('exam_hall_panel/', views.exam_hall_panel, name='exam_hall_panel'),
    path('create_exam_hall/', views.create_exam_hall, name='create_exam_hall'),
    path('edit_exam_hall/<int:pk>/', views.edit_exam_hall, name='edit_exam_hall'),
    path('delete_exam_hall/<int:pk>/', views.delete_exam_hall, name='delete_exam_hall'),
    path('delete_all_exam_halls/', views.delete_all_exam_halls, name='delete_all_exam_halls'),
    path('upload_exam_halls/', views.upload_exam_halls, name='upload_exam_halls'),
    
    # Exam Supervisor URLs
    path('exam-supervisors/', views.exam_supervisor_panel, name='exam_supervisor_panel'),
    path('exam-supervisors/create/', views.create_exam_supervisor, name='create_exam_supervisor'),
    path('exam-supervisors/edit/<int:pk>/', views.edit_exam_supervisor, name='edit_exam_supervisor'),
    path('exam-supervisors/delete/<int:pk>/', views.delete_exam_supervisor, name='delete_exam_supervisor'),
    path('exam-supervisors/delete-all/', views.delete_all_exam_supervisors, name='delete_all_exam_supervisors'),
    path('exam-supervisors/upload/', views.upload_exam_supervisors, name='upload_exam_supervisors'),
    
    # Scheduling URLs
    path('schedule/', views.schedule, name='schedule'),
    path('invigilators/create/', views.create_invigilator, name='create_invigilator'),
    path('invigilators/edit/<int:pk>/', views.edit_invigilator, name='edit_invigilator'),
    path('supervisors/create/', views.create_supervisor, name='create_supervisor'),
    path('supervisors/edit/<int:pk>/', views.edit_supervisor, name='edit_supervisor'),
    
    # Committee URLs
    path('committee-dashboard/', views.committee_dashboard, name='committee_dashboard'),
    
    # Conflict Management URLs
    path('conflicts/', views.conflict_dashboard, name='conflict_dashboard'),
    path('conflicts/resolve/<int:pk>/', views.resolve_conflict, name='resolve_conflict'),
    path('conflicts/lecturer/<int:lecturer_id>/', views.lecturer_conflicts, name='lecturer_conflicts'),
    path('conflicts/supervisor/<int:supervisor_id>/', views.supervisor_conflicts, name='supervisor_conflicts'),
    path('conflicts/hall/<int:hall_id>/', views.hall_conflicts, name='hall_conflicts'),
    path('conflicts/lecturer-report/<int:lecturer_id>/', views.lecturer_conflicts_report, name='lecturer_conflicts_report'),
    path('conflicts/supervisor-report/<int:supervisor_id>/', views.supervisor_conflicts_report, name='supervisor_conflicts_report'),
    path('conflicts/hall-report/<int:hall_id>/', views.hall_conflicts_report, name='hall_conflicts_report'),
    
    # Notification URLs
    path('notifications/', views.notifications_view, name='notifications'),
    
    # Report URLs
    path('reports/backend/', views.reports_backend, name='reports_backend'),
    path('reports/frontend/', views.reports_frontend, name='reports_frontend'),
    path('notifications/', views.notifications_view, name='notifications_list'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)