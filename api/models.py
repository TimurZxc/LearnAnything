from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings
 
class CustomManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    def delete(self, *args, **kwargs):
        self.token_set.all().delete()
        super().delete(*args, **kwargs)


class User(AbstractUser):
    username = None
    surname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(_("email address"), max_length=150,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    objects = CustomManager()
    is_mentor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Student(models.Model):
    user = models.OneToOneField(User, related_name='student', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

class Course(models.Model):
    name = models.CharField(max_length=200)
    student = models.ForeignKey(Student, related_name="course", on_delete=models.CASCADE)

class Topic(models.Model):
    name = models.CharField(max_length=200)
    is_opened = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    course = models.ForeignKey(Course, related_name="topic", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.name)
    
class Video(models.Model):
    link = models.URLField()
    topic = models.ForeignKey(Topic, related_name="video", on_delete=models.CASCADE)

class Source(models.Model):
    link = models.URLField()
    topic = models.ForeignKey(Topic, related_name="source", on_delete=models.CASCADE)

class Quiz(models.Model):
    topic = models.ForeignKey(Topic, related_name="quiz", on_delete=models.CASCADE)

class Question(models.Model):
    body = models.TextField()
    option_1 = models.TextField()
    option_2 = models.TextField()
    option_3 = models.TextField()
    option_4 = models.TextField()
    correct = models.CharField(max_length=10)
    quiz = models.ForeignKey(Quiz, related_name="question", on_delete=models.CASCADE)

class Test(models.Model):
    user = models.ForeignKey(User, related_name="test", on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, related_name="course", on_delete=models.CASCADE, null=True) 
    question = models.TextField()
    option_1 = models.TextField()
    option_2 = models.TextField()
    option_3 = models.TextField()
    option_4 = models.TextField()
    correct = models.CharField(max_length=100)