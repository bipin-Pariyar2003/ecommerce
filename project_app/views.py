from django.shortcuts import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required


#Home page--------------------------------------------------------------------------
def index(request):
    queryset= Product.objects.all()
    print("-------query set", queryset)
    
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
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=request.user)
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

#----------------------check out----------------------------------------
@login_required
def calculate_total_price(cart_items):
    total_price = sum(item.quantity * item.product.product_price for item in cart_items)
    return total_price

@login_required
def checkout(request):
    print("REQ", request)
    print("USER", request.user)
    user = request.user  # Retrieve the user from the request


    if request.method == 'POST':
        # Logic to confirm order and create an Order instance
        # cart_items = CartItem.objects.filter(cart__user=user)
        cart_items = CartItem.objects.prefetch_related('cart__user').filter(cart__user=user)
        print("CART ITEMS", cart_items)
        total_price = calculate_total_price(cart_items)

        # Create an Order instance
        order = Order.objects.create(user=user, total_price=total_price)
        print("ORDER", order)
        

        # Add cart items to the order
        order.items.add(*cart_items)

        # Clear the user's cart
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation')

    # elif request.method == 'GET':
    #     # Fetch the user's address and phone number from the User model
    #     address = user.user_address
    #     phone_number = user.user_phone

    #     # Fetch the items in the user's cart
    #     cart_items = CartItem.objects.filter(cart__user=user)
    #     print("CART ITEMS", cart_items)

    #     # Calculate the total price of items in the user's cart
    #     total_price = calculate_total_price(cart_items)
    #     print("TOTAL PRICES", total_price)
        

    #     context = {
    #         'address': address,
    #         'phone_number': phone_number,
    #         'cart_items': cart_items,
    #         'total_price': total_price,
    #     }
    #     print('CONTEXT', context)
    #     return render(request, 'checkout.html', context)
    
    elif request.method == 'GET':
        # Pre-fetch user data
        cart_items = CartItem.objects.prefetch_related('cart__user').filter(cart__user=user)
        print("CART ITEMS", cart_items)

        # Access user object for each item (optional, not needed for rendering)
        # for item in cart_items:
        #     user = item.cart.user

        # Fetch the user's address and phone number from the User model
        address = user.user_address
        print("address----", address)
        phone_number = user.user_phone
        print("phone----", phone_number)

        # Calculate the total price of items in the user's cart
        # total_price = calculate_total_price(cart_items)
        total_price = sum(item.quantity * item.product.product_price for item in cart_items)
        
        # print("totalPrice----", total_price)

        # Build context for template rendering
        context = {
            'address': address,
            'phone_number': phone_number,
            'cart_items': cart_items,
            'total_price': total_price,
        }
        print("CONTEXT", context)

        # Render the checkout template
        return render(request, 'checkout.html', context)



#Thankyou
def thankyou(request):
    return render(request, "thankyou.html", {})