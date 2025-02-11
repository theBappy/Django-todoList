from django.urls import path
from .views import task_list, complete_task, delete_task, task_update, register, login_view, logout_view

urlpatterns = [
     path('', task_list, name='task_list'),  
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('completed/<int:task_id>/', complete_task, name='complete-task'),
    path('delete/<int:task_id>/', delete_task, name='delete-task'),
    path('update/<int:task_id>/', task_update, name='task-update'),
]