from django.urls import path, include
from .views import (
    GoalListApiView,
    GoalDetailApiView
)

urlpatterns = [
    path('', GoalListApiView.as_view()),
    path('<int:goal_id>/', GoalDetailApiView.as_view())
]
