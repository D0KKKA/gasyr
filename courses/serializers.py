from rest_framework import serializers
from courses import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Course
        fields='__all__'

class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserCourse
        fields='__all__'


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.VideoLesson
        fields='__all__'


class UserLessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLessonProgress
        fields = '__all__'


