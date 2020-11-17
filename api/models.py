from django.db import models


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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name
