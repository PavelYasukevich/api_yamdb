from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        ]


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=255)


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
    rating = serializers.SerializerMethodField('calc_rating')

    def calc_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerWrite(serializers.ModelSerializer):
    """Запись данных в таблицу Title"""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', required=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ['title']
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = self.context['request'].parser_context['kwargs'][
                'title_id'
            ]
            author = self.context['request'].user
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ['review_id']
        model = Comment
