from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter  
from django_filters.rest_framework import DjangoFilterBackend   
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, 
    CartItemSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # --- THESE ARE THE MAGIC LINES THAT WERE MISSING! ---
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'stock'] 
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer