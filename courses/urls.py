from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseListCreateView, CourseViewSet, LessonCreateView, LessonDetailView, UserCourseViewSet
app_name = 'courses'
router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='courses')

router.register(r'user-courses', UserCourseViewSet, basename='user-courses')

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:course_id>/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
]

# Добавляем урлы из роутера
urlpatterns += router.urls
