from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Q

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=255, help_text=_("Duration in days"))

    def update_completion_percentage_for_user(self, user):
        total_lessons = self.lessons.count()
        completed_lessons = self.user_courses.filter(user=user, completed_on__gte=100).count()
        if total_lessons > 0:
            completion_percentage = (completed_lessons / total_lessons) * 100
            UserCourse.objects.filter(user=user, course=self).update(completed_on=completion_percentage)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to="lesson_videos")

    def update_completion_percentage_for_user(self, user):
        total_tasks = self.code_tasks.count() + self.test_tasks.count()
        completed_tasks = self.user_tasks.filter(
            Q(code_task__is_correct=True) |
            Q(test_task__is_correct=True)
        ).count()
        if total_tasks > 0:
            completion_percentage = (completed_tasks / total_tasks) * 100
            UserLessonTask.objects.filter(user=user, lesson=self).update(completed_on=completion_percentage)

    def __str__(self):
        return self.title

class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_on = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} - {self.course}"

class CodeTask(models.Model):
    lesson = models.OneToOneField(Lesson, related_name='code_task', on_delete=models.CASCADE)
    description = models.TextField()
    input_data = models.CharField(max_length=255)
    output_data = models.CharField(max_length=255)

    def __str__(self):
        return f"Code for Lesson: {self.lesson.title}"

class TestTask(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='test_tasks', on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(choices=((1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')))

class UserLessonTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='user_tasks', on_delete=models.CASCADE)
    code_task = models.ForeignKey(CodeTask, related_name='user_code_tasks', on_delete=models.CASCADE)
    test_task = models.ForeignKey(TestTask, related_name='user_test_tasks', on_delete=models.CASCADE)
    solution_code = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_on = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"User: {self.user.username}, Lesson: {self.lesson.title}"
