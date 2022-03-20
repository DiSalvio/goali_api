from django.urls import path, include
from .views import (
    GoalListApiView,
    GoalDetailApiView,
    TaskListApiView,
    TaskDetailApiView
)

urlpatterns = [
    # path('', GoalListApiView.as_view()),
    # path('<int:goal_id>/', GoalDetailApiView.as_view()),
    # path('', TaskListApiView.as_view()),
    # path('<int:goal_id>/task/<int:task_id>', TaskDetailApiView.as_view())
]
