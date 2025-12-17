
from django.urls import path
from . import views

urlpatterns = [
    # Lecturer URLs
    path('create_lecturer/', views.create_lecturer, name='create_lecturer'),
    path('edit_lecturer/<int:pk>/', views.edit_lecturer, name='edit_lecturer'),
    path('delete_lecturer/<int:pk>/', views.delete_lecturer, name='delete_lecturer'),
    path('delete_all_lecturers/', views.delete_all_lecturers, name='delete_all_lecturers'),

    # Exam Hall Assignment URLs
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
]