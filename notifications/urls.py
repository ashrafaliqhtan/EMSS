# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('notifications/mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    # notifications/urls.py
    path('notifications/count/', views.notification_count, name='notification_count'),
]