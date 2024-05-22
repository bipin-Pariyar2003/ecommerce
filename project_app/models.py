from django.db import models

# Create your models here.

#User
class User(models.Model):
    user_name=models.CharField(max_length=200)
    user_email=models.CharField(max_length=200)
    user_password=models.CharField(max_length=200)
    user_address=models.CharField(max_length=200)
    user_phone=models.IntegerField()

#Product
class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.IntegerField()
    product_discount=models.IntegerField()
    product_description=models.CharField(max_length=200)
    product_image=models.ImageField(upload_to="product")

    
#Category
class Category(models.Model):
    
    category_name=models.CharField(max_length=200)
    category_description=models.CharField(max_length=200)
    