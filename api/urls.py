<<<<<<< HEAD
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

router_v1 = DefaultRouter()
router_v1.register("users", views.MyUserViewSet, basename="users")

auth_patterns = [
    path("email/", views.get_confirmation_code, name="get_confirmation_code"),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
]

urlpatterns = [
    path("v1/auth/", include(auth_patterns)),
    path("v1/users/me/", views.SelfMyUserViewSet.as_view()),
    path("v1/", include(router_v1.urls)),
=======
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
>>>>>>> develop/content
]
