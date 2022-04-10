from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from goali.models import SubTask
from ..serializers import SubTaskSerializer


class SubTaskListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        sub_tasks = SubTask.objects.filter(
            goal=self.kwargs.get('goal_id'),
            task=self.kwargs.get('task_id'),
            user=request.user.id
        )
        serializer = SubTaskSerializer(sub_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'completed': request.data.get('completed'),
            'goal': self.kwargs.get('goal_id'),
            'task': self.kwargs.get('task_id'),
            'user': request.user.id
        }
        serializer = SubTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, sub_task_id, goal_id, task_id, user_id):
        try:
            return SubTask.objects.get(
                id=sub_task_id,
                goal=self.kwargs.get('goal_id'),
                task=self.kwargs.get('task_id'),
                user=user_id
            )
        except SubTask.DoesNotExist:
            return None

    def put(self, request, sub_task_id, *args, **kwargs):
        sub_task_instance = self.get_object(
            sub_task_id,
            self.kwargs.get('goal_id'),
            self.kwargs.get('task_id'),
            request.user.id
        )
        if not sub_task_instance:
            return Response(
                {"res": "Object with subtask id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "name": request.data.get('name'),
            "description": request.data.get('description'),
            "completed": request.data.get('completed'),
            "removed": request.data.get('removed'),
            "goal": self.kwargs.get('goal_id'),
            "task": self.kwargs.get('task_id'),
            "user": request.user.id
        }
        serializer = SubTaskSerializer(instance=sub_task_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, sub_task_id, *args, **kwargs):
        sub_task_instance = self.get_object(
            sub_task_id,
            self.kwargs.get('goal_id'),
            self.kwargs.get('task_id'),
            request.user.id
        )
        if not sub_task_instance:
            return Response(
                {"res": "Object with subtask id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubTaskSerializer(sub_task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, sub_task_id, *args, **kwargs):
        sub_task_instance = self.get_object(
            sub_task_id,
            self.kwargs.get('goal_id'),
            self.kwargs.get('task_id'),
            request.user.id
        )
        if not sub_task_instance:
            return Response(
                {"res": "Object with sub task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        sub_task_instance.delete()
        return Response(
            {"res": "SubTask Object deleted!"},
            status=status.HTTP_200_OK
        )
