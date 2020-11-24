from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint


class MyUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def _create_user(
        self, email, username=None, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class Roles(models.TextChoices):
    user = "user"
    moderator = "moderator"
    admin = "admin"
    django_admin = "django_admin"


class MyUser(AbstractUser):
    email = models.EmailField(
        max_length=50,
        help_text="Электронная почта пользователя",
        verbose_name="Электронная почта",
        unique=True,
    )
    bio = models.CharField(
        max_length=255,
        help_text="Информация о пользователе",
        verbose_name="Информация",
        blank=True,
    )
    role = models.CharField(
        choices=Roles.choices,
        default="user",
        max_length=50,
        help_text="Права пользователя",
        verbose_name="Права",
    )

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_django_admin(self):
        return self.role == "django_admin"

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['email']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


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


class Review(models.Model):

    def validate_score(value):
        if 10 < value < 1:
            raise ValidationError('Оценка должна между 1 и 10.')

    author = models.ForeignKey(
        MyUser,
        help_text="Автор отзыва",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )

    title = models.ForeignKey(
        Title,
        help_text="Произведение, на которое сделан отзыв",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )

    text = models.TextField(
        help_text="Отзыв пользователя",
        verbose_name="Отзыв",
    )
    score = models.PositiveSmallIntegerField(
        help_text="Оценка пользователя",
        validators=[validate_score],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Дата добавления отзыва",
        verbose_name="Дата добавления",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name="unique_review",
            )
        ]
        ordering = ['title']
        verbose_name = "Отзыв пользователя"
        verbose_name_plural = "Отзывы пользователей"

    def __str__(self):
        fragment = (
            self.text if len(self.text) <= 50 else self.text[:50] + "..."
        )
        date = self.pub_date.strftime("%d %m %Y")
        author = self.author
        return f"{author} - {date} - {fragment}"


class Comment(models.Model):
    author = models.ForeignKey(
        MyUser,
        help_text="Автор комментария",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    text = models.TextField(
        help_text="Комментарий пользователя",
        verbose_name="Комментарий",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Дата добавления комментария",
        verbose_name="Дата добавления",
    )
    review_id = models.ForeignKey(
        Review,
        help_text="Комментируемый отзыв",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментируемый отзыв",
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Комментарий пользователя"
        verbose_name_plural = "Комментарии пользователей"

    def __str__(self):
        fragment = (
            self.text if len(self.text) <= 50 else self.text[:50] + "..."
        )
        date = self.pub_date.strftime("%d %m %Y")
        author = self.author
        return f"{author} - {date} - {fragment}"