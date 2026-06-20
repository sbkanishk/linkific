from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Spin up the router for the blog
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]