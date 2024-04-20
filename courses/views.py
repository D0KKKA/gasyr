from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .models import Course, Lesson, UserCourse
from .permissions import IsAdminOrReadOnly,IsAuthenticatedOrReadOnly
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    UserCourseSerializer
)

class CourseListCreateView(generics.ListCreateAPIView):
    """
    Список всех курсов и создание нового курса:
    для создания курса нужно быть авторизованным
    Ответ:
    - id: Идентификатор курса.
    - title: Название курса.
    - description: Описание курса.
    - price: Цена курса.
    - duration: Продолжительность курса в днях.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        """
        Описание: Получает список всех курсов и позволяет создать новый курс.
        Параметры для создания:
        - title (обязательный): Название курса.
        - description (обязательный): Описание курса.
        - price (обязательный): Цена курса.
        - duration (обязательный): Продолжительность курса в днях.
        """
        if request.user.is_authenticated:
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Только зарегистрированные пользователи могут создавать курсы"}, status=status.HTTP_401_UNAUTHORIZED)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'id'


class LessonCreateView(generics.CreateAPIView):
    """
    Создание урока:

    Описание: Создает новый урок для указанного курса.
    Параметры:
    - course_id (в URL): Идентификатор курса.
    - title (обязательный): Название урока.
    - video (обязательный): Видео урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_url_kwarg = 'course_id'

    def post(self, request, course_id):
        course = generics.get_object_or_404(Course, id=course_id)
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, редактирование и удаление урока:

    Описание: Получает данные, редактирует и удаляет урок.
    Параметры:
    - course_id (в URL): Идентификатор курса.
    - lesson_id (в URL): Идентификатор урока.

    Ответ:
    - id: Идентификатор урока.
    - title: Название урока.
    - video: Видео урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_url_kwarg = 'lesson_id'


class UserCourseViewSet(viewsets.ModelViewSet):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'id'

