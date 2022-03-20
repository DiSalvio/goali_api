from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from goali.models import Task
from ..serializers import TaskSerializer


class TaskListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(goal=self.kwargs.get('goal_id'), user=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'completed': request.data.get('completed'),
            'goal': self.kwargs.get('goal_id'),
            'user': request.user.id
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, task_id, goal_id, user_id):
        try:
            return Task.objects.get(id=task_id, goal=self.kwargs.get('goal_id'), user=user_id)
        except Task.DoesNotExist:
            return None

    def put(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id, self.kwargs.get('goal_id'), request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "name": request.data.get('name'),
            "description": request.data.get('description'),
            "completed": request.data.get('completed'),
            "goal": self.kwargs.get('goal_id'),
            "user": request.user.id
        }
        serializer = TaskSerializer(instance=task_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id, self.kwargs.get('goal_id'), request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id, self.kwargs.get('goal_id'), request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response(
            {"res": "Task Object deleted!"},
            status=status.HTTP_200_OK
        )
