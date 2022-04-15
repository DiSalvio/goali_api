from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from goali.models import Goal
from ..serializers import GoalSerializer


class GoalListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        goals = Goal.objects.filter(user=request.user.id)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = GoalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, goal_id, user_id):
        try:
            return Goal.objects.get(id=goal_id, user=user_id)
        except Goal.DoesNotExist:
            return None

    def put(self, request, goal_id, *args, **kwargs):
        goal_instance = self.get_object(goal_id, request.user.id)
        if not goal_instance:
            return Response(
                {"res": "Object with goal id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "name": request.data.get('name'),
            "description": request.data.get('description'),
            "completed": request.data.get('completed'),
            "removed": request.data.get('removed'),
            "user": request.user.id
        }
        serializer = GoalSerializer(instance=goal_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, goal_id, *args, **kwargs):
        goal_instance = self.get_object(goal_id, request.user.id)
        if not goal_instance:
            return Response(
                {"res": "Object with goal id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GoalSerializer(goal_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, goal_id, *args, **kwargs):
        goal_instance = self.get_object(goal_id, request.user.id)
        if not goal_instance:
            return Response(
                {"res": "Object with goal id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        goal_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
