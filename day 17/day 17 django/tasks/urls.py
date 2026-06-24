from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import TaskViewSet, RegisterViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterViewSet.as_view({'post': 'create'})),
    path('auth/login/', obtain_auth_token),
]