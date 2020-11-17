from rest_framework import serializers

from api.models import Title, Genre, Category


class GenresSerializer(serializers.ModelSerializer):
    """Вывод жанров"""
    class Meta:
        model = Genre
        exclude = ('id',)


class CategoriesSerializer(serializers.ModelSerializer):
    """Вывод категорий"""
    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializeRead(serializers.ModelSerializer):
    """Вывод данных таблицы Title"""
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleSerializerWrite(serializers.ModelSerializer):
    """Запись данных в таблицу Title"""
    genre = serializers.SlugRelatedField(slug_field='slug', many=True, required=True, queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug', required=True, queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
