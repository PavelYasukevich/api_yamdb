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
]
