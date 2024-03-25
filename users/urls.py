from django.urls import path, include
from rest_framework import routers
from users import views
app_name = 'users'

# Создание экземпляра маршрутизатора
router = routers.DefaultRouter()

# Регистрация представлений в маршрутизаторе
router.register(r'users', views.UserView)
router.register(r'phones', views.PhoneView)

urlpatterns = [
    # Включение маршрутов из маршрутизатора
    path('', include(router.urls)),
    path('registration/',views.RegistrationView.as_view(),name='user-registration')
]
