from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users import models,serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken ,AccessToken

class UserView(viewsets.ModelViewSet):
    queryset= models.User.objects.all()
    serializer_class=serializers.UserSerializer


class PhoneView(viewsets.ModelViewSet):
    queryset = models.Phone.objects.all()
    serializer_class = serializers.PhoneSerializer


User = get_user_model()
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer= serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






