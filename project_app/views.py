from django.shortcuts import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required

#Home page--------------------------------------------------------------------------
def index(request):
    queryset= Product.objects.all()
    
    #for search operation
    search = request.GET.get("search")
    if search:
        queryset= queryset.filter(product_name__icontains = search)
        
    data = Category.objects.all()
        
    context={'page':"Home", "all_products": queryset, 'data':data}
    return render(request,"index.html", context)

#------------------- LOG OUT -----------------------------------------------
def log_out(request):
    logout(request)
    return redirect('/login/')
    
    
    
#--------------------------------------- REGISTER ----------------------------------------------------------------------
User= get_user_model()

def register(request):
    if request.method=="POST":
        username= request.POST.get("username")
        email= request.POST.get("email")
        password= request.POST.get("password")
        user_address= request.POST.get("user_address")
        user_phone= request.POST.get("user_phone")
        #validations
        user = User.objects.filter(email=email)
        if user.exists():
            messages.info(request, "Email Id already used.")
            return redirect("/register/")
        # if not password.len()>=6:
        #     messages.info(request, "Password length should be equal or greater than 6")
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_address=user_address,
            user_phone=user_phone
        )
        
        messages.info(request, "Registered Successfully!!")
        return redirect("/register/")
    
    queryset= User.objects.all()
    context={'page':"Register", "register": queryset}
    return render(request, "register.html", context)

#------------------------------------- LOG IN ---------------------------------------------------------------

def log_in(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password= request.POST.get("password")
        
        # if not User.objects.filter(email=email).exists():
        #     messages.error(request, "Invalid Details!!")
        #     return redirect("/login/")
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            messages.error(request, "Invalid Details!!")
            return redirect("/login/")  
        
        else:
            login(request, user)
            if user.is_superuser:
                return redirect("/admin/")
            else:     
                return redirect("/index/")
            
    context={'page':"LogIn"}    
    return render(request, "login_page.html", context)

#------------------------CART--------------------------------
#Add to cart
@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.info(request, "Product Added to Cart")
    return redirect('/index/')


#view cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.product.product_price for item in cart_items)
    
    
    context = {
        'cart_items': cart_items, 'total_price': total_price
    }
    return render(request, 'view_cart.html', context)

#update cart
@login_required
def update_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
    return redirect('view_cart')


#remove from cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('/cart/')



#--------------------------- CheckOUT-----------------------------------------
@login_required
def checkout(request):
    if request.method == 'GET':
        # Assuming you have a UserProfile model associated with each user
        user_profile = request.user.userprofile

        # Assuming UserProfile model has fields like address, phone_number, etc.
        context = {
            'user_profile': user_profile,
            'total_price': calculate_total_price(request.user)
        }
        return render(request, 'checkout.html', context)
    
    elif request.method == 'POST':
        # Logic to confirm order, update database, etc.
        # This could involve creating an Order model, updating product quantities, etc.
        # Once the order is confirmed, you may want to clear the user's cart
        clear_cart(request.user)
        return redirect('order_confirmation')  # Redirect to a page confirming the order
    
#calculate total price
def calculate_total_price(user):
    # Logic to calculate total price of items in user's cart
    total_price = 0
    cart_items = user.cart.cartitem_set.all()
    for item in cart_items:
        total_price += item.quantity * item.product.product_price
    return total_price

#clear cart
def clear_cart(user):
    # Logic to clear user's cart after placing an order
    user.cart.cartitem_set.all().delete()