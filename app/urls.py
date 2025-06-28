from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path("", views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('export_excel/', views.export_excel, name='export_excel'),  
    path('dashboard/',views.dashboard,name='dashboard'),
    path('settings/',views.settings,name='settings'),
]