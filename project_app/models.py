from django.db import models

# Create your models here.

#User
class User(models.Model):
    full_name=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    user_email=models.CharField(max_length=200)
    user_password=models.CharField(max_length=200)
    user_address=models.CharField(max_length=200)
    user_phone=models.IntegerField()
    def __str__(self):
        return self.full_name
    

#Product
class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.IntegerField()
    product_discount=models.IntegerField()
    product_description=models.CharField(max_length=200)
    product_image=models.ImageField(upload_to="product")
    def __str__(self):
        return self.product_name

    
#Category
class Category(models.Model):
    
    category_name=models.CharField(max_length=200)
    category_description=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name_name
    