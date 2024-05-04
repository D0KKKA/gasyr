from drf_yasg import openapi
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from .models import *
from .permissions import *
from .serializers import *

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_classes = [IsAdminOrReadOnly]


    @swagger_auto_schema(
        operation_summary='создать курс',
        responses={status.HTTP_201_CREATED: CourseSerializer()},
    )
    def post(self, request, *args, **kwargs):
        """
        Создать новый курс
        """
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'

    # @swagger_auto_schema()
    # def create(self, request, *args, **kwargs):
    #     """
    #     Создать новый курс
    #     """
    #     return super().create(request, *args, **kwargs)
    #
    # @swagger_auto_schema()
    # def update(self, request, *args, **kwargs):
    #     """
    #     Обновить информацию о курсе
    #     """
    #     return super().update(request, *args, **kwargs)
    #
    # @swagger_auto_schema()
    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     Частично обновить информацию о курсе
    #     """
    #     return super().partial_update(request, *args, **kwargs)
    #
    # @swagger_auto_schema()
    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Удалить курс
    #     """
    #     return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def list_lessons_by_course_id(self, request, id=None):
        course = self.get_object()
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)




class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    #permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = 'course_id'

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: LessonSerializer()},
    )

    def post(self, request, course_id):
        """
               Создать новый урок для курса
               """
        course = get_object_or_404(Course, id=course_id)
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_url_kwarg = 'lesson_id'

    @swagger_auto_schema()
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию о уроке
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema()
    def update(self, request, *args, **kwargs):
        """
        Обновить информацию о уроке
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema()
    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновить информацию о уроке
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema()
    def destroy(self, request, *args, **kwargs):
        """
        Удалить урок
        """
        return super().destroy(request, *args, **kwargs)




class UserCourseViewSet(viewsets.ModelViewSet):

    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'


    @action(detail=False, methods=['get'])
    def paid_courses(self, request):
        """
        Получить список оплаченных пользовательских курсов
        """
        user = request.user
        paid_courses = self.queryset.filter(user=user, is_paid=True)
        serializer = self.get_serializer(paid_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CodeTaskCreateView(generics.CreateAPIView):
    queryset=CodeTask.objects.all()
    serializer_class = CodeTaskSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(
        request_body=CodeTaskSerializer,
        responses={status.HTTP_201_CREATED: CodeTaskSerializer()},
    )

    def post(self, request, lesson_id):
        """
        Создать новую задачу на код для урока
        """
        lesson = get_object_or_404(Lesson, id=lesson_id)
        serializer = CodeTaskSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save(lesson=lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodeTask.objects.all()
    serializer_class = CodeTaskSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Обновить информацию о задаче на код",
        request_body=CodeTaskSerializer,
        responses={status.HTTP_200_OK: CodeTaskSerializer()}
    )

    @swagger_auto_schema()
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию о задаче на код
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CodeTaskSerializer)
    def update(self, request, *args, **kwargs):
        """
        Обновить информацию о задаче на код
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema()
    def destroy(self, request, *args, **kwargs):
        """
        Удалить задачу на код
        """
        return super().destroy(request, *args, **kwargs)


class TestTaskCreateView(generics.CreateAPIView):
    queryset = TestTask.objects.all()
    serializer_class = TestTaskSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(
        request_body=TestTaskSerializer,
        responses={status.HTTP_201_CREATED: TestTaskSerializer()},
    )
    def post(self, request, lesson_id):
        """
            Создать новую тестовую задачу для урока
        """
        lesson = get_object_or_404(Lesson, id=lesson_id)
        serializer = TestTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lesson=lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestTask.objects.all()
    serializer_class = TestTaskSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema()
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию о тестовой задаче
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=TestTaskSerializer)
    def update(self, request, *args, **kwargs):
        """
        Обновить информацию о тестовой задаче
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema()
    def destroy(self, request, *args, **kwargs):
        """
        Удалить тестовую задачу
        """
        return super().destroy(request, *args, **kwargs)



class TestTaskSubmitView(APIView):
    #permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_answer': openapi.Schema(type=openapi.TYPE_STRING),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['user_answer', 'task_id'],
        ),
        responses={status.HTTP_200_OK: UserLessonTaskSerializer()},
    )


    def post(self, request, task_id):
        """
               Проверить ответ на тестовую задачу
               """
        user_answer = request.data.get('user_answer')
        test_task = get_object_or_404(TestTask, id=task_id)
        correct_option = test_task.correct_option

        if user_answer == correct_option:
            is_correct = True
        else:
            is_correct = False

        # Create or update UserLessonTask for the user
        user = request.user
        lesson = test_task.lesson
        user_lesson_task, created = UserLessonTask.objects.get_or_create(
            user=user,
            lesson=lesson,
            test_task=test_task
        )
        user_lesson_task.is_correct = is_correct
        user_lesson_task.save()

        serializer = UserLessonTaskSerializer(user_lesson_task)
        return Response(serializer.data)

class CodeTaskSubmitView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_code': openapi.Schema(type=openapi.TYPE_STRING),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['user_code', 'task_id'],
        ),
        responses={status.HTTP_200_OK: UserLessonTaskSerializer()},
    )
    #permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        """
               Проверить ответ на задачу на код
               """
        user_code = request.data.get('user_code')
        code_task = get_object_or_404(CodeTask, id=task_id)
        expected_output = code_task.output_data


        user_output = True#execute_code(user_code, code_task.input_data)

        if user_output == expected_output:
            is_correct = True
        else:
            is_correct = False


        user = request.user
        lesson = code_task.lesson
        user_lesson_task, created = UserLessonTask.objects.get_or_create(
            user=user,
            lesson=lesson,
            code_task=code_task
        )
        user_lesson_task.is_correct = is_correct
        user_lesson_task.save()

        serializer = UserLessonTaskSerializer(user_lesson_task)
        return Response(serializer.data)

class UserLessonTaskViewSet(viewsets.ModelViewSet):
    queryset = UserLessonTask.objects.all()
    serializer_class = UserLessonTaskSerializer
    #permission_classes = [IsAdminOrAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(operation_summary="Получить информацию о пользовательской задаче урока")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Создать новую пользовательскую задачу урока")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Обновить информацию о пользовательской задаче урока")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Удалить пользовательскую задачу урока")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class UserLessonStatusView(APIView):
    '''
    получить статус просмотра урока пользователем
    '''
    def get(self, request, lesson_id):
        user = request.user
        try:
            user_lesson = UserLesson.objects.get(user=user, lesson_id=lesson_id)
            serializer = UserLessonSerializer(user_lesson)
            return Response(serializer.data)
        except UserLesson.DoesNotExist:
            return Response({"message": "Урок не найден"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, lesson_id):
        '''
        обновляет статус просмотра курса
        принимает параметры 'viewed', 'not_viewed', 'started' и lesson_id

        '''

        user = request.user
        try:
            user_lesson = UserLesson.objects.get(user=user, lesson_id=lesson_id)
            view_status = request.data.get('view_status')
            if view_status in ['viewed', 'not_viewed', 'started']:
                user_lesson.view_status = view_status
                user_lesson.save()
                serializer = UserLessonSerializer(user_lesson)
                return Response(serializer.data)
            else:
                return Response({"message": "Неправильный статус просмотра"}, status=status.HTTP_400_BAD_REQUEST)
        except UserLesson.DoesNotExist:
            return Response({"message": "Урок не найден"}, status=status.HTTP_404_NOT_FOUND)

class UserLessonViewSet(viewsets.ModelViewSet):
    serializer_class = UserLessonSerializer
    queryset = UserLesson.objects.all()

class TopicView(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()