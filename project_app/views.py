from django.shortcuts import *
from django.http import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


def index(request):
    queryset= Product.objects.all()
    
    #for search operation
    search = request.GET.get("search")
    if search:
        queryset= queryset.filter(product_name__icontains = search)
        
    context={'page':"Home", "all_products": queryset}
    return render(request,"index.html", context)


def log_in(request):
    if request.method=="POST":
        user_email=request.POST.get("user_email")
        user_password= request.POST.get("user_password")
        
        user = authenticate(request, username=user_email, password=user_password)
        
        if user is None:
            messages.error(request, "Invalid Details!!")
            return redirect("/login/")
        
        else:
            login(request, user)
            return redirect("/index/")
            
    
    context={'page':"LogIn"}    
    return render(request, "login.html", context)

def register(request):
    if request.method=="POST":
        user_name= request.POST.get("user_name")
        user_email= request.POST.get("user_email")
        user_password= request.POST.get("user_password")
        user_address= request.POST.get("user_address")
        user_phone= request.POST.get("user_phone")
        
        user = User.objects.filter(user_email=user_email)
        if user.exists():
            messages.info(request, "Email Id already used.")
            return redirect("/register/")
        
        User.objects.create(
            user_name=user_name,
            user_email=user_email,
            user_password=user_password,
            user_address=user_address,
            user_phone=user_phone
        )
        
        messages.info(request, "Registered Successfully!!")
        return redirect("/register/")
    
    queryset= User.objects.all()
    context={'page':"Register", "register": queryset}
    return render(request, "register.html", context)



def add_product(request):
    if request.method=="POST":
        product_name=request.POST.get("product_name")
        product_price=request.POST.get("product_price")
        product_discount=request.POST.get("product_discount")
        product_description=request.POST.get("product_description")
        product_image=request.FILES.get("product_image")
        
        Product.objects.create(
            product_name=product_name,
            product_price=product_price,
            product_discount=product_discount,
            product_description=product_description,
            product_image=product_image
        )

        return redirect("/index/")
        
    queryset=Product.objects.all()
    context= {'page': "add-product","add_product":queryset}
    return render(request, "add_product.html", context)


def delete_product(request, id):
    queryset= Product.objects.get(id=id)
    queryset.delete()
    return redirect("/index/")


def update_product(request, id):
    queryset=Product.objects.get(id=id)
    context={"product": queryset}
    if request.method=="POST":
        product_name=request.POST.get("product_name")
        product_price=request.POST.get("product_price")
        product_discount=request.POST.get("product_discount")
        product_description=request.POST.get("product_description")
        product_image=request.FILES.get("product_image")
        
        queryset.product_name=product_name
        queryset.product_price=product_price
        queryset.product_discount=product_discount
        queryset.product_description=product_description
        
        if product_image:
            queryset.product_image=product_image
        
        queryset.save()
        return redirect("/index/")

    return render(request, "update_product.html", context)