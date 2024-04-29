from django.urls import path, include
from rest_framework import routers
from .views import *
app_name = 'users'

# Создание экземпляра маршрутизатора
router = routers.DefaultRouter()

# Регистрация представлений в маршрутизаторе
router.register(r'users', UserView)
router.register(r'notifications', NotificationsViewSet)


urlpatterns = [
    # Включение маршрутов из маршрутизатора
    path('', include(router.urls)),
    path('registration/',RegistrationView.as_view(),name='user-registration'),
    path('login/',LoginView.as_view(),name='user-login'),
    path('logout/',LogoutView.as_view(),name='user-logout'),
    path('profile/',UserProfileView.as_view(),name='user-profile'),
    path('notifications/', NotificationsListCreateView.as_view(), name='notifications-list-create'),
    path('notifications/<int:pk>/', NotificationsDetailView.as_view(), name='notifications-detail'),
]


