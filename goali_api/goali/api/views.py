from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from goali.models import Goal
from .serializers import GoalSerializer, SignUpSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


class SignUpApiView(APIView):
    def get(self, request):
        return Response({'Message': 'This is get method of signup API'}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            obj = SignUpSerializer(data = request.data)
            if obj.is_valid():
                obj.save()
                return Response({'Message': 'Successfully Signed up'}, status=status.HTTP_200_OK)
            return Response(obj.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Message': f'Failed due to {e}'}, status=status.HTTP_400_BAD_REQUEST)

class GoalListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        goals = Goal.objects.filter(user = request.user.id)
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
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            "name": request.data.get('name'),
            "description": request.data.get('description'),
            "completed": request.data.get('completed'),
            "user": request.user.id
        }
        serializer = GoalSerializer(instance = goal_instance, data=data, partial=True)
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

