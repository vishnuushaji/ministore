from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"    


class Smartphone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    storage_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.brand} {self.model}"

class Smartwatch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    water_resistant = models.BooleanField()

    def __str__(self):
        return f"{self.brand} {self.model}"
    
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateField()
    category = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Generate a unique slug based on the title
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    quote = models.TextField()
    rating = models.FloatField()
    author_name = models.CharField(max_length=255)

    def __str__(self):
        return self.author_name