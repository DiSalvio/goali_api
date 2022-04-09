"""goali_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from goali.api.views import (
    login,
    logout,
    SignUpApiView,
    GoalListApiView,
    GoalDetailApiView,
    TaskListApiView,
    TaskDetailApiView,
    SubTaskListApiView,
    SubTaskDetailApiView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('goals/', GoalListApiView.as_view()),
    path('goals/<int:goal_id>/', GoalDetailApiView.as_view()),
    path('goals/<int:goal_id>/tasks/', TaskListApiView.as_view()),
    path('goals/<int:goal_id>/tasks/<int:task_id>/', TaskDetailApiView.as_view()),
    path('goals/<int:goal_id>/tasks/<int:task_id>/subtasks/', SubTaskListApiView.as_view()),
    path('goals/<int:goal_id>/tasks/<int:task_id>/subtasks/<int:sub_task_id>/', SubTaskDetailApiView.as_view()),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', login),
    path('signup/', SignUpApiView.as_view()),
    path('logout/', logout)
]
