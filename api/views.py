from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from . import serializers
from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .permissions import (CustomerAccessPermission, IsAdmin,
                          ReviewCommentPermission)


User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = serializers.EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if User.objects.filter(email=serializer.data["email"]).exists():
        return Response(
            {"error": "User with this email already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    confirmation_code = default_token_generator.make_token(request.user)

    User.objects.create(
        email=serializer.data["email"], password=confirmation_code
    )
    send_mail(
        "Your confirmation code",
        confirmation_code,
        [serializer.data["email"]],
    )
    return Response(
        {"email": serializer.data["email"]},
        status=status.HTTP_200_OK,
    )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = serializers.MyTokenObtainPairSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = serializers.MyUserSerializer
    lookup_field = "username"
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get("username", None)
        if username:
            queryset = queryset.filter(username=username)
        return queryset


class SelfMyUserViewSet(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MyUserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        obj = get_object_or_404(queryset, id=user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class TitleViewSet(viewsets.ModelViewSet):
    """
    Таблица: Title
    Разрешеные методы: GET, POST, PUT, PATCH, DELETE
    Доступ: GET - Нет ограничений
            POST, PUT, PATCH, DELETE - admin
    """

    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = (CustomerAccessPermission,)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return serializers.TitleSerializeRead
        else:
            return serializers.TitleSerializerWrite


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Таблица: Category
    Разрешеные методы: GET, POST, DELETE
    Доступ: GET - Нет ограничений
            POST, DELETE - admin
    """

    queryset = Category.objects.all()
    serializer_class = serializers.CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    permission_classes = (CustomerAccessPermission,)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Category, slug=self.kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Таблица: Genre
    Разрешеные методы: GET, POST, DELETE
    Доступ: GET - Нет ограничений
            POST, DELETE - admin
    """

    queryset = Genre.objects.all()
    serializer_class = serializers.GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    permission_classes = (CustomerAccessPermission,)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Genre, slug=self.kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return serializer.save(author=self.request.user, review_id=review)
