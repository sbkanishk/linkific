from django.shortcuts import render
from django.views.generic import ListView  # <--- We added this import!
from .models import Product

def store_home(request):
    # 1. Grab all products from the database
    all_products = Product.objects.all()
    
    # 2. Package them up and send them to an HTML file
    return render(request, 'store_home.html', {'products': all_products})

# --- NEW: CLASS-BASED VIEW ---
class ProductListView(ListView):
    model = Product
    template_name = 'store_home.html' 
    context_object_name = 'products'