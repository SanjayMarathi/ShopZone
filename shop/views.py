from django.shortcuts import render, redirect
from .models import Products, Order 
from django.core.paginator import Paginator
from django.db import transaction 
import json 
# Create your views here.

def index(request):
    product_objects = Products.objects.all()
    # ... (rest of index view remains unchanged) ...
    
    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)
    
    #paginator code
    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)    
        
    return render(request,'shop/index.html', {'product_objects':product_objects})

def detail(request, id):
    product_object = Products.objects.get(id=id)
    return render(request, 'shop/detail.html', {
        'product_object':product_object
    })

def cart(request):
    product_objects = Products.objects.all()
    return render(request, 'shop/cart.html', {'product_objects': product_objects})

# MODIFIED: Checkout view now handles two steps
def checkout(request):
    if request.method == 'POST':
        # --- STEP 2: FINALIZE PAYMENT & DEDUCT STOCK ---
        try:
            # 1. Collect form data
            customer_name = request.POST.get('customer_name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            zip_code = request.POST.get('zip_code')
            cart_data_json = request.POST.get('cart_data', '{}')
            cart = json.loads(cart_data_json)

            if not cart:
                return render(request, 'shop/checkout.html', {'status': 'error', 'message': 'Your cart is empty.'})
            
            # Basic validation for new fields
            if not all([customer_name, email, address, zip_code]):
                 return render(request, 'shop/checkout.html', {
                    'status': 'error',
                    'message': 'Missing required shipping information (Name, Email, Address, or ZIP Code).'
                })


            with transaction.atomic():
                # 2. Create Order record (before stock deduction)
                Order.objects.create(
                    name=customer_name,
                    email=email,
                    address=address,
                    zip_code=zip_code,
                    cart_data=cart_data_json
                )

                # 3. Deduct Stock
                for product_id, quantity in cart.items():
                    product = Products.objects.select_for_update().get(id=int(product_id))
                    
                    if product.stock < quantity:
                        # Rollback is handled by transaction.atomic() on exception
                        return render(request, 'shop/checkout.html', {
                            'status': 'error',
                            'message': f'Insufficient stock for {product.title}. Only {product.stock} available.'
                        })

                    product.stock -= quantity
                    product.save()

            return render(request, 'shop/checkout.html', {
                'status': 'success',
                'message': 'Order successful! Stock updated and order details saved in the database.'
            })

        except Products.DoesNotExist:
            return render(request, 'shop/checkout.html', {'status': 'error', 'message': 'One or more products were not found.'})
        except Exception as e:
            print(f"Checkout error: {e}")
            return render(request, 'shop/checkout.html', {'status': 'error', 'message': 'An unexpected error occurred during checkout.'})

    # --- STEP 1: ORDER SUMMARY / PAYMENT PAGE (GET Request) ---
    product_objects = Products.objects.all()
    return render(request, 'shop/checkout.html', {'product_objects': product_objects, 'is_summary_page': True})