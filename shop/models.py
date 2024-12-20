from django.db import models
from django.contrib.auth import get_user_model

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=255, default='default_category')

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="wishlisted")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="carted")
    quantity = models.PositiveIntegerField(default=1)
    @property 
    def total_price(self): 
        return self.product.price * self.quantity 
    @property 
    def estimated_delivery(self): return '3-5 business days' # Example estimated delivery

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"
class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='products/extra/')

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    text_review = models.TextField(blank=True, null=True)
    image_review = models.ImageField(upload_to='reviews/images/', blank=True, null=True)
    video_review = models.FileField(upload_to='reviews/videos/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)  # Rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"