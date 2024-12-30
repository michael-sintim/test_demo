from django.urls import path
from .views import TodoDetailView, TodoListView

urlpatterns = [
    path('api/todos/', TodoListView.as_view(), name='todo-list'),
    path('api/todos/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
]
