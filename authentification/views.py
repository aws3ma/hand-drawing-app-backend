from django.contrib.auth.models import User
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

class SignUp(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class Account(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data
        user = User.objects.get(id=request.user.id)
        ser = UserSerializer(user, data=data,partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user = UserSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)