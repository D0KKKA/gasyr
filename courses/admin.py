from django.contrib import admin
from . import models

admin.site.register(
    models.Course
)
admin.site.register(
    models.Lesson
)
admin.site.register(
    models.CodeTask
)
admin.site.register(
    models.TestTask
)
admin.site.register(
    models.UserLessonTask
)
admin.site.register(
    models.UserCourse
)

