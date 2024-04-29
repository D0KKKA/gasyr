from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import RegexValidator, MinValueValidator,MaxValueValidator
from datetime import date, timedelta
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


USER = "user"
ADMIN = "admin"

ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
]
phone_reg = RegexValidator(
    regex=r'^(\+?7|8)(\d{10})$',

    message="Номер телефона должен быть в формате: '+71234567890'. "
)



class User(AbstractUser):
    objects = CustomUserManager()
    username= None
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to="users_photo")
    role = models.CharField(default=USER, choices=ROLES, max_length=9)
    password_repeat = models.CharField(max_length=128)

    phone = models.CharField(validators=[phone_reg], max_length=16, unique=True)
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(date.today() - timedelta(days=365 * 100)),
            MaxValueValidator(date.today()),
        ],
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff


    @property
    def is_user(self):
        return self.is_authenticated and self.role == USER


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    def toggle_favorite(self):
        self.is_favorite = not self.is_favorite
        self.save()

    def __str__(self):
        return self.title

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


