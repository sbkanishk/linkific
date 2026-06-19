from django.urls import path
from . import views
from .views import ProductListView  # <--- We added this import!

urlpatterns = [
    # Your original Function-Based View
    path('', views.store_home, name='home'), 
    
    # --- NEW: Your Class-Based View ---
    path('class-view/', ProductListView.as_view(), name='class_home'), 
]