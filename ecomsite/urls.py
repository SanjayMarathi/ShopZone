# ShopZone/ecomsite/urls.py

"""
URL configuration for ecomsite project.
...
"""
from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    # Added cart and checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'), 
    # NEW URL: for generating QR code dynamically
    path('generate-upi-qr/', views.generate_upi_qr, name='generate_upi_qr'),
]