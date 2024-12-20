from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
    path('checkout/', views.checkout_view, name='checkout'), 
    path('process_payment/', views.process_payment, name='process_payment'),
    path('search/',  views.product_search, name='search'), 
    path('category/<str:category_name>/', views.category_view, name='category'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),  # Add contact URL
    path('terms/', views.terms, name='terms'),  
]

