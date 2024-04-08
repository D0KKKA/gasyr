from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses import views

router = DefaultRouter()
router.register(r'courses', views.CourseView)
router.register(r'user-courses', views.UserCourseView)
router.register(r'video-lessons', views.VideoLessons)
router.register(r'user-lesson-progress', views.UserLessonProgressViewSet)



urlpatterns = [
    path('',include(router.urls)),

]
