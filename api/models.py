from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def _create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class MyUser(AbstractUser):
    class Roles(models.TextChoices):
        anon = "anon"
        user = "user"
        moderator = "moderator"
        admin = "admin"
        django_admin = "django_admin"

    email = models.EmailField(max_length=25, unique=True)
    bio = models.CharField(max_length=25, blank=True)
    role = models.CharField(max_length=12, choices=Roles.choices, default="user")

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Genre(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ("-year",)

    def __str__(self):
        return self.name
