from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import login
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from courses import models,serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .permissions import IsAdminOrReadOnly


# Create your views here.
class CourseView(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer = serializers.CourseSerializer
    permission_classes = [IsAuthenticated]



class UserCourseView(viewsets.ModelViewSet):
    queryset = models.UserCourse.objects.all()
    serializer =serializers.UserCourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='add-course')
    def add_course_to_user(self, request, pk=None):
        user = self.get_object()
        course_id = request.data.get('course_id')
        course = get_object_or_404(models.Course, pk=course_id)
        user_course, created = models.UserCourse.objects.get_or_create(user=user, course=course)
        serializer = self.get_serializer(user_course)
        return Response(serializer.data)

class VideoLessons(viewsets.ModelViewSet):
    queryset = models.VideoLesson.objects.all()
    serializer = serializers.VideoLessonSerializer
    permission_classes = [IsAuthenticated]


class UserLessonProgressViewSet(viewsets.ModelViewSet):
    queryset = models.UserLessonProgress.objects.all()
    serializer_class = serializers.UserLessonProgressSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            course_id = serializer.validated_data['course']
            lesson_id = serializer.validated_data['lesson']
            lesson = get_object_or_404(models.VideoLesson, pk=lesson_id)
            if not user.usercourse_set.filter(course_id=course_id).exists():
                return Response({"error": "You are not enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
            user_progress, created = models.UserLessonProgress.objects.get_or_create(
                user=user,
                course_id=course_id,
                lesson_id=lesson_id,
                defaults={'completed': serializer.validated_data.get('completed', False)}
            )
            if not created:
                user_progress.completed = serializer.validated_data.get('completed', False)
                user_progress.save()
            serializer = self.get_serializer(user_progress)
            return Response(serializer.data)






    