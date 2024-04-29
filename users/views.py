from rest_framework import viewsets, status
from rest_framework.generics import DestroyAPIView, CreateAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from users import models, serializers
from users.models import Notifications
from users.serializers import NotificationsSerializer
from rest_framework.decorators import action
User = get_user_model()


class UserView(viewsets.ModelViewSet):
    """
    Предоставляет CRUD-операции для пользователей.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class RegistrationView(APIView):
    """
    Регистрирует нового пользователя.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.UserRegistrationSerializer,
        responses={status.HTTP_201_CREATED: "User registered successfully"}
    )
    def post(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Авторизует пользователя.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=serializers.LoginSerializer,
        responses={status.HTTP_200_OK: "Authentication successful"}
    )
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            login(request, user)
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
    """
    Выход пользователя из системы.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: "Logout successful"})
    def post(self, request):
        logout(request)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token_type, refresh_token = auth_header.split(' ', 1)
            if token_type and refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    return Response({'error': 'Invalid Refresh token'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Refresh token missing'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Предоставляет профиль пользователя и позволяет его обновить.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: "User profile retrieved successfully"}
    )
    def get(self, request):
        try:
            user_profile = request.user
            serializer = serializers.UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=serializers.UserProfileSerializer,
        responses={status.HTTP_200_OK: "User profile updated successfully"}
    )
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


class NotificationsListCreateView(ListCreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notifications.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notifications.objects.filter(user=user)


class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_unread()
        return Response({'detail': 'Notification marked as unread.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        notification = self.get_object()
        notification.toggle_favorite()
        return Response({'detail': 'Notification favorite status toggled.'}, status=status.HTTP_200_OK)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = models.Notes.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)