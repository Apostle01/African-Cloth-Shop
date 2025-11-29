from django.db import models
from django.contrib.auth.models import User
import datetime

# Category of Products
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    #@Codemy2025
    class Meta:
        verbose_name_plural = 'categories'
   

# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password =  models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# All of our Products
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, max_length=250, default='', null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/products/', blank=True, null=True, default='images/red-kente.JPG')

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    quantity = models.IntegerField(default=1) 
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today) 
    status = models.BooleanField(default=-False)

    def __str__(self):
        return self.product 

