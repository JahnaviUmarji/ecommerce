from django.db import models
from datetime import datetime

class AuditData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# Create your models here.
class Product(AuditData):  # Renamed to singular (Django convention)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed data type
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL, null=True, related_name='product')
    
class Category(AuditData):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Orders(AuditData):
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False)
    total_amount = models.DecimalField(max_digits=10,decimal_places=3)
    products = models.ManyToManyField(Product,related_name='Product')

