from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Category, Genre, Title

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "bio", "email", "role"]


class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=255)

    def validate(self, data):
        user = get_object_or_404(
            User, email=data["email"], password=data["confirmation_code"]
        )

        refresh = RefreshToken.for_user(user)

        return {"access": str(refresh.access_token)}


class GenresSerializer(serializers.ModelSerializer):
    """Вывод жанров"""

    class Meta:
        model = Genre
        exclude = ("id",)


class CategoriesSerializer(serializers.ModelSerializer):
    """Вывод категорий"""

    class Meta:
        model = Category
        exclude = ("id",)


class TitleSerializeRead(serializers.ModelSerializer):
    """Вывод данных таблицы Title"""

    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")


class TitleSerializerWrite(serializers.ModelSerializer):
    """Запись данных в таблицу Title"""

    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, required=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", required=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")
