from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import SignUpSerializer

class SignUpApiView(APIView):
    def get(self, request):
        return Response({'Message': 'This is get method of Sign Up API'}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            obj = SignUpSerializer(data = request.data)
            if obj.is_valid():
                obj.save()
                return Response({'Message': 'Successfully Signed up'}, status=status.HTTP_200_OK)
            return Response(obj.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Message': f'Failed due to {e}'}, status=status.HTTP_400_BAD_REQUEST)
