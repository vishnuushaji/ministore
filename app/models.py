from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)  
    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (${self.product.price})"
    
from django.utils import timezone

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateField()
    category = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    quote = models.TextField()
    rating = models.FloatField()
    author_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.author_name
    

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id}"

    def total_quantity(self):
        return sum(item.quantity for item in self.order_items.all())

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"OrderItem {self.id} ({self.quantity} x {self.product.name})"


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"