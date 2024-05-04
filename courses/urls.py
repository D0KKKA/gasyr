from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:course_id>/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('courses/<int:lesson_id>/code_tasks/', CodeTaskCreateView.as_view(), name='code-task-create'),
    path('courses/<int:lesson_id>/test_tasks/', TestTaskCreateView.as_view(), name='test-task-create'),

    path('courses/<int:lesson_id>/code_tasks/<int:code_task_id>', CodeTaskDetailView.as_view(), name='code-task-detail'),
    path('courses/<int:lesson_id>/test_tasks/<int:test_task_id>', TestTaskDetailView.as_view(), name='test-task-detail'),


    path('test_tasks/<int:task_id>/submit/', TestTaskSubmitView.as_view(), name='test-task-submit'),
    path('code_tasks/<int:task_id>/submit/', CodeTaskSubmitView.as_view(), name='code-task-submit'),

    path('lessons/<int:lesson_id>/status/', UserLessonStatusView.as_view(), name='user_lesson_status'),
]

router = DefaultRouter()
router.register(r'user_lesson_tasks', UserLessonTaskViewSet, basename='user-lesson-task')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'user_courses', UserCourseViewSet, basename='user-course')
router.register(r'topic', TopicView, basename='topic')
router.register(r'user_lesson', UserLessonViewSet, basename='user-lesson')

urlpatterns += router.urls
