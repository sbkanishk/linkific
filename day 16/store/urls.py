from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Spin up the magic switchboard
router = DefaultRouter()

# 2. Plug in all the ViewSets we just built
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cart-items', views.CartItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'reviews', views.ReviewViewSet)

# 3. Tell Django to use the switchboard for all URLs in this app
urlpatterns = [
    path('', include(router.urls)),
]