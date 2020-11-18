from django.contrib.auth import get_user_model
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

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .permissions import CustomerAccessPermission, IsAdmin, MethodAccessPermission
from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    EmailSerializer,
    GenresSerializer,
    MyTokenObtainPairSerializer,
    MyUserSerializer,
    ReviewSerializer,
    TitleSerializeRead,
    TitleSerializerWrite,
)

User = get_user_model()


def generate_confirmation_code():
    from secrets import token_hex

    return token_hex(10)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():

        if User.objects.filter(email=serializer.data["email"]).exists():
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        confirmation_code = generate_confirmation_code()

        User.objects.create(
            email=serializer.data["email"], password=confirmation_code
        )
        send_mail(
            "Your confirmation code",
            confirmation_code,
            "noreply@yamdb.com",
            [serializer.data["email"]],
        )
        return Response(
            {"message": "Confirmation code has been sent to your email"},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = MyUserSerializer
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
    serializer_class = MyUserSerializer

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
            return TitleSerializeRead
        else:
            return TitleSerializerWrite


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
    serializer_class = CategoriesSerializer
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
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    permission_classes = (CustomerAccessPermission,)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Genre, slug=self.kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (MethodAccessPermission,) 

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset = Review.objects.filter(title_id=title)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return serializer.save(author=self.request.user, title_id=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset = Comment.objects.filter(title_id=title)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return serializer.save(author=self.request.user, title_id=title)
