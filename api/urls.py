from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, CategoryViewSet, GenreViewSet


title_router = DefaultRouter()
category_router = DefaultRouter()
genre_router = DefaultRouter()

title_router.register('', TitleViewSet, basename='titles')
category_router.register('', CategoryViewSet, basename='categories')
genre_router.register('', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/titles/', include(title_router.urls)),
    path('v1/categories/', include(category_router.urls)),
    path('v1/genres/', include(genre_router.urls)),
]
