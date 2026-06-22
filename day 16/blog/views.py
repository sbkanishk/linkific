from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from .models import Author, Post, Comment
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # <--- Import your custom permission class

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # <--- Requires token authentication

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Combines both: Public can read, authenticated users can write, but ONLY the owner can edit/delete
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # <--- Requires token authentication