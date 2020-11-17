from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ('-year',)
    def __str__(self):
        return self.name

class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews")
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews")
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True)

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True)
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments")
