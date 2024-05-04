from rest_framework import serializers
from courses import models

from rest_framework import serializers
from .models import *

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class UserCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = UserCourse
        fields = '__all__'

class CodeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeTask
        fields = '__all__'

class TestTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTask
        fields = '__all__'

class UserLessonTaskSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    class Meta:
        model = UserLessonTask
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserLessonSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    class Meta:
        model = UserLesson
        fields = ['view_status',"lesson"]