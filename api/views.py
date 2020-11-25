from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (CustomerAccessPermission, IsAdmin,
                          ReviewCommentPermission)

User = get_user_model()


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = serializers.EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = default_token_generator.make_token(request.user)
    User.objects.create(
        email=serializer.validated_data['email'], password=confirmation_code
    )
    send_mail(
        'Your confirmation code',
        confirmation_code,
        [serializer.data['email']],
    )
    return Response(serializer.data)


@api_view(['POST'])
def get_token(request):
    serializer = serializers.TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, email=email)

    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)})
    return Response(
        {'confirmation_code': 'Указан неверный код подтверждения.'}
    )


class MyUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = serializers.MyUserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    queryset = User.objects.all()

    @action(
        url_path='me',
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def profile(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
        if self.action in ['list', 'retrieve']:
            return serializers.TitleSerializeRead
        return serializers.TitleSerializerWrite


class AvailableMethods(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ Исключен `retrieve()` метод."""
    pass


class CategoryViewSet(AvailableMethods):
    """
    Таблица: Category
    Разрешеные методы: GET, POST, DELETE
    Доступ: GET - Нет ограничений
            POST, DELETE - admin
    """
    queryset = Category.objects.all()
    serializer_class = serializers.CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = (CustomerAccessPermission,)

    def get_object(self):
        if self.action == 'destroy':
            obj = get_object_or_404(Category, slug=self.kwargs['pk'])
            return obj



class GenreViewSet(AvailableMethods):
    """
    Таблица: Genre
    Разрешеные методы: GET, POST, DELETE
    Доступ: GET - Нет ограничений
            POST, DELETE - admin
    """

    queryset = Genre.objects.all()
    serializer_class = serializers.GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = (CustomerAccessPermission,)

    def get_object(self):
        if self.action == 'destroy':
            obj = get_object_or_404(Genre, slug=self.kwargs['pk'])
            return obj


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return serializer.save(author=self.request.user, review_id=review)
