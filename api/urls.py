from django.urls import include, path
from rest_framework.routers import DefaultRouter 

from . import views 
 
v1_router = DefaultRouter() 
v1_router.register('reviews', views.ReviewViewSet, basename='reviews') 
v1_router.register('titles', views.ReviewViewSet, basename='titles') 
v1_router.register('comments', views.ReviewViewSet, basename='comments') 



from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
    
urlpatterns = [
        path('v1/', include(v1_router.urls)),
        path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ] 


