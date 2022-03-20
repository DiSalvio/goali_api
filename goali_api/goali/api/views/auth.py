from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import SignUpSerializer
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
