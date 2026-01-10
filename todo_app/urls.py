from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('delete/<int:id>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:id>/', views.toggle_todo, name='toggle_todo'),
]
