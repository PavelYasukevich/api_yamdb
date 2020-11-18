from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register("users", views.MyUserViewSet, basename="users")
router_v1.register("titles", views.TitleViewSet, basename="titles")
router_v1.register("categories", views.CategoryViewSet, basename="categories")
router_v1.register("genres", views.GenreViewSet, basename="genres")
router_v1.register("reviews", views.ReviewViewSet, basename="reviews")
router_v1.register("comments", views.ReviewViewSet, basename="comments")

auth_patterns = [
    path("email/", views.get_confirmation_code, name="get_confirmation_code"),
    path(
        "token/",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]

urlpatterns = [
    path("v1/auth/", include(auth_patterns)),
    path("v1/users/me/", views.SelfMyUserViewSet.as_view()),
    path("v1/", include(router_v1.urls)),
]
