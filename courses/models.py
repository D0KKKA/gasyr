from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator,MinValueValidator,FileExtensionValidator


class Course(models.Model):
    title=models.CharField(max_length=150,blank=False)
    description=models.TextField()
    duration=models.DurationField(max_length=255,blank=False)
    students = models.ManyToManyField(User, through='UserCourse')
    price=models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],  # Минимальное значение цены
        blank=False,
        default=0
    )


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class VideoLesson(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='video_lessons')
    image=models.ImageField(
        upload_to='Media/'
    )
    video_url = models.FileField(
        upload_to='Media/Video',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    create_at=models.DateTimeField(auto_now_add=True)


class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(VideoLesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
