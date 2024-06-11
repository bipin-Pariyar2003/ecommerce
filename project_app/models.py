from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please provide a valid Email!!")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    user_address = models.CharField(max_length=200)
    user_phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        return self.username  
    
    def __str__(self):
        return self.username
    
    
    #Category
class Category(models.Model):
    
    category_name=models.CharField(max_length=200)
    category_description=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

#Product
class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.IntegerField()
    product_discount=models.IntegerField()
    product_description=models.CharField(max_length=200)
    product_image=models.ImageField(upload_to="product")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name

    

    