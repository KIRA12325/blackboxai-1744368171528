from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.medicine_list_view, name='medicine_list'),
    path('add/', views.add_medicine_view, name='add_medicine'),
    path('<int:pk>/', views.medicine_detail_view, name='medicine_detail'),
    path('<int:pk>/edit/', views.edit_medicine_view, name='edit_medicine'),
    path('<int:pk>/delete/', views.delete_medicine_view, name='delete_medicine'),
    
    path('reminders/', views.reminder_list_view, name='reminder_list'),
    path('reminders/add/', views.add_reminder_view, name='add_reminder'),
    path('reminders/<int:pk>/', views.reminder_detail_view, name='reminder_detail'),
    path('reminders/<int:pk>/edit/', views.edit_reminder_view, name='edit_reminder'),
    path('reminders/<int:pk>/delete/', views.delete_reminder_view, name='delete_reminder'),
    
    path('scan/', views.scan_view, name='scan'),
    path('scan/history/', views.scan_history_view, name='scan_history'),
    path('scan/process/', views.process_scan_view, name='process_scan'),
]
