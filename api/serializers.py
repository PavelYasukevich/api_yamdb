from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        ]


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
    rating = serializers.SerializerMethodField("calc_rating")

    def calc_rating(self, obj):
        return obj.reviews.aggregate(Avg("score"))["score__avg"]

    class Meta:
        model = Title
        fields = "__all__"


class TitleSerializerWrite(serializers.ModelSerializer):
    """Запись данных в таблицу Title"""

    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        required=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", required=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        exclude = ["title"]
        model = Review

    def validate(self, data):
        title = self.context["view"].kwargs["title_id"]
        author = self.context["request"].user
        if self.context["request"].method == "POST":
            if Review.objects.filter(
                author=author, title=title
            ).exists():
                raise serializers.ValidationError("Вы уже оставили отзыв")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        exclude = ["review_id"]
        model = Comment
