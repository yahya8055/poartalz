from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Wishlist, Cart , Order
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .forms import ReviewForm

from django.shortcuts import render
from .models import Product

from django.shortcuts import render
from .models import Product
'''
def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'shop/product_list.html', {'products': products})
'''
def product_search(request):
    query = request.GET.get('q', '')  # Get the search query
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.none()  # Empty QuerySet if no search query
    return render(request, 'shop/search_results.html', {'products': products, 'query': query})

def category_view(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'shop/product_list.html', {'products': products})


'''def product_list(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'query': query}'''


def home_view(request):
    products = Product.objects.all() 
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')  # Ensure 'about.html' exists in templates

def contact(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')
'''
def search_view(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'shop/product_search.html', {'products': products, 'query': query})

def category_view(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'shop/product_list.html', {'products': products})
'''

def cart_view(request):
    cart_items = Cart.objects.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        item.estimated_delivery = '3-5 business days'  # Example estimated delivery
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

'''def cart_view(request):
    cart_items = Cart.objects.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'shop/cart.html', {'cart_items': cart_items})
'''
'''
def update_cart(request, item_id):
    if request.method == 'POST':
        item = Cart.objects.get(id=item_id)
        item.quantity = request.POST['quantity']
        item.save()
    return redirect('cart')
    

'''
def update_cart(request, item_id):
    if request.method == 'POST':
        item = Cart.objects.get(id=item_id)
        data = json.loads(request.body)
        item.quantity = data['quantity']
        item.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

def checkout_view(request):
    cart_items = Cart.objects.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        item.estimated_delivery = '3-5 business days'  # Example estimated delivery
    return render(request, 'shop/checkout.html', {'cart_items': cart_items})

def process_payment(request):
    if request.method == 'POST':
        # Process payment here
        return redirect('payment_success')
    return redirect('checkout')


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = Cart.objects.get(id=item_id)
        item.delete()
    return redirect('cart')
    

def wishlist_view(request):
    wishlist_items = Wishlist.objects.all()
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

def remove_from_wishlist(request, item_id):
    if request.method == 'POST':
        item = Wishlist.objects.get(id=item_id)
        item.delete()
    return redirect('wishlist')

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        Cart.objects.create(product=product, quantity=1)
    return redirect('cart')




# List all products
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# View product details
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    reviews = product.reviews.all()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        review_form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'images': images,
        'reviews': reviews,
        'review_form': review_form,
    })

# View wishlist
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

# Add to wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

# View cart
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

# Add to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# Checkout
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity
            )
        cart_items.delete()  # Clear the cart after checkout
        return redirect('product_list')  # Redirect to product list after checkout
    return render(request, 'shop/checkout.html', {'cart_items': cart_items})
