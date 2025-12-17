from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import exam_list, create_exam, edit_exam, delete_exam, upload_exams, exam_detail
from .views import (
    conflict_dashboard,
    resolve_conflict,
    lecturer_conflicts_report,
    supervisor_conflicts_report,
    hall_conflicts_report
)
urlpatterns = [
    path('', views.homePage, name='home'),
    path('user-login', views.userlogin, name='login'),
    path('logout', views.userlogout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard1', views.dashboard1, name='dashboard1'),
    path('halls', views.halls, name='halls'),
    # path('departments', views.departments, name='departments'),
    path('lecturers', views.lecturers, name='lecturers'),
    path('schedule', views.schedule, name='schedule'),
    # path('Upload-departments', views.upload_department, name='upload_department'),
    path('Upload-halls', views.upload_hall, name='upload_hall'),
    path('Upload-lecturers', views.upload_lecturers, name='upload_lecturers'),
    path('invigilator/create/', views.create_invigilator, name='create_invigilator'),
    path('exams/', exam_list, name='exam_list'),
    path('exams/create/', create_exam, name='create_exam'),
    path('exams/edit/<int:pk>/', edit_exam, name='edit_exam'),
    path('exams/delete/<int:pk>/', delete_exam, name='delete_exam'),
    path('exams/upload/', upload_exams, name='upload_exams'),
    #path('exams/<int:pk>/', exam_detail, name='exam_detail'),  # Ensure this exists
    path('notifications/', views.notifications_view, name='notifications_list'),
    path('reports/backend/', views.reports_backend, name='reports_backend'),
    path('reports/frontend/', views.reports_frontend, name='reports_frontend'),
    
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),

    path("invigilator/edit/<int:pk>/", views.edit_invigilator, name="edit_invigilator"),
    path("supervisor/create/", views.create_supervisor, name="create_supervisor"),
    path("supervisor/edit/<int:pk>/", views.edit_supervisor, name="edit_supervisor"),

    path("hall/create/", views.create_hall, name="create_hall"),
    path("hall/edit/<int:pk>/", views.edit_hall, name="edit_hall"),
    path('create_lecturer/', views.create_lecturer, name='create_lecturer'),
    path('edit_lecturer/<int:pk>/', views.edit_lecturer, name='edit_lecturer'),
    path('delete_lecturer/<int:pk>/', views.delete_lecturer, name='delete_lecturer'),
    path('delete_all_lecturers/', views.delete_all_lecturers, name='delete_all_lecturers'),

    # http://127.0.0.1:8000/create_lecturer/
    path('exam_hall_panel/', views.exam_hall_panel, name='exam_hall_panel'),
    path('create_exam_hall/', views.create_exam_hall, name='create_exam_hall'),
    path('edit_exam_hall/<int:pk>/', views.edit_exam_hall, name='edit_exam_hall'),
    path('delete_exam_hall/<int:pk>/', views.delete_exam_hall, name='delete_exam_hall'),
    path('delete_all_exam_halls/', views.delete_all_exam_halls, name='delete_all_exam_halls'),
    path('upload_exam_halls/', views.upload_exam_halls, name='upload_exam_halls'),

    # Exam Supervisor URLs
    path('exam_supervisor_panel/', views.exam_supervisor_panel, name='exam_supervisor_panel'),
    path('create_exam_supervisor/', views.create_exam_supervisor, name='create_exam_supervisor'),
    path('edit_exam_supervisor/<int:pk>/', views.edit_exam_supervisor, name='edit_exam_supervisor'),
    path('delete_exam_supervisor/<int:pk>/', views.delete_exam_supervisor, name='delete_exam_supervisor'),
    path('delete_all_exam_supervisors/', views.delete_all_exam_supervisors, name='delete_all_exam_supervisors'),
    path('upload_exam_supervisors/', views.upload_exam_supervisors, name='upload_exam_supervisors'),
    
    path('supervisors/<int:supervisor_id>/conflicts/', views.supervisor_conflicts, name='supervisor_conflicts'),
    
    # Conflict Management URLs



    path('conflicts/', conflict_dashboard, name='conflict_dashboard'),
    path('conflicts/<int:pk>/resolve/', resolve_conflict, name='resolve_conflict'),
    path('conflicts/lecturer/<int:lecturer_id>/', lecturer_conflicts_report, name='lecturer_conflicts_report'),
    path('conflicts/supervisor/<int:supervisor_id>/', supervisor_conflicts_report, name='supervisor_conflicts_report'),
    path('conflicts/hall/<int:hall_id>/', hall_conflicts_report, name='hall_conflicts_report'),
    
    
        
    path('signup/', views.signup, name='signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
