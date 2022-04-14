from rest_framework import status
from rest_framework.response import Response
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
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def logout(request):
    token = request.data.get("token")
    if token is None:
        return Response({'error': 'Please provide token'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        db_token = Token.objects.get(key=token)
    except Token.DoesNotExist:
        db_token = None
    if db_token is None:
        return Response(
            {"res": "Object with token does not exist"},
            status=status.HTTP_400_BAD_REQUEST
        )
    db_token.delete()
    return Response(
        {"res": "Token deleted!"},
        status=status.HTTP_200_OK
    )
