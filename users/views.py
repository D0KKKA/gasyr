from django.shortcuts import render
from django.contrib.auth import login
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from users import models,serializers
from django.contrib.auth import get_user_model , authenticate,logout
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
        serializer= serializers.UserRegistrationSerializer(data=request.data)
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








class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user :
            login(request,user)


            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'email': user.email
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Обычно заголовок Authorization имеет формат "Bearer <token>",
            # поэтому мы разделяем его и берем вторую часть
            token_type, refresh_token = auth_header.split(' ', 1)
            if token_type and refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    return Response({'error': 'Неверный Refresh token'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)
        return Response({'error': 'Отсутствует Refresh token'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = request.user
            serializer = serializers.UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            user_profile = request.user
            serializer = serializers.UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
