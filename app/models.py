from django.db import models
# from common.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
# in settings -> settings unit
from django.utils import timezone
from datetime import datetime
import datetime
import ast
from django.db.models import Manager
from django.db.models import Count, F, Value


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def _str_(self):
        return f'{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country}'

class Degree(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Department(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Book(models.Model):
    img = models.ImageField(null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    isbn = models.CharField(max_length=13, unique=True,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    year = models.PositiveIntegerField(default=0,null=True,blank=True)
    semester = models.PositiveIntegerField(default=0,null=True,blank=True)
    stock = models.PositiveIntegerField(null=True,blank=True)
    published_date = models.DateField(null=True,blank=True)
    department = models.ForeignKey(Department,null=True,blank=True,on_delete=models.CASCADE)

    def _str_(self):
        return self.title

    def update_stock(self, quantity):
        if quantity < 0 and abs(quantity) > self.stock:
            raise ValueError("Cannot reduce stock below zero")
        self.stock += quantity
        self.save()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,null=True,blank=True)
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def _str_(self):
        return f'Review by {self.user.username} for {self.book.title}'

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def change_quantity(self, quantity):
        self.quantity = quantity
        self.save()
        
    def _str_(self):
        return f'{self.quantity} of {self.book.title} in cart'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    is_paid = models.BooleanField(default=False,null=True,blank=True)
    is_shipped = models.BooleanField(default=False,null=True,blank=True)
    is_delivered = models.BooleanField(default=False,null=True,blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)

    def _str_(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,null=True,blank=True)   
    quantity = models.PositiveIntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    
    def _str_(self):
        return f'{self.quantity} of {self.book.title} in order {self.order.id}'