from django.shortcuts import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import re
from django.db.models import Prefetch

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
        
        if not len(password)>=6:
            messages.info(request, "Password length should be equal or greater than 6")
            return redirect("/register/")
        
        if not re.match(r'^(98|97)\d{8}$', user_phone):
            messages.error(request, "Phone number must start with 98 or 97 and be 10 digits long.")
            return redirect("/register/")
        
        
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_address=user_address,
            user_phone=user_phone,
            is_active=False
        )
        
        # messages.info(request, "Registered Successfully!!")
        # return redirect("/register/")
        messages.info(request, "Registration pending admin approval.")
        return redirect("/login/")
    
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
            if cart_item.quantity > 1:  # Check if quantity is greater than 1
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
    user = request.user  # Retrieve the current user from the request

    if request.method == 'POST':
        cart_items = CartItem.objects.filter(cart__user=user)
        total_price = sum(item.quantity * item.product.product_price for item in cart_items)

        # Create the order
        order = Order.objects.create(user=user, total_price=total_price)

        # Associate cart items with the order
        order_items = []
        for cart_item in cart_items:
            order.items.add(cart_item)  # Add each cart item to the order
            order_items.append(cart_item.product.product_name)  # Collect item names for logging or other purposes

        # Clear the user's cart
        cart_items.delete()

        # Optionally, you can log the order items for tracking purposes
        print(f"Order #{order.id} items: {', '.join(order_items)}")
        print(f"Order {order_items}")
        print(f"OrderItems {order.items}")

        messages.success(request, "Order placed successfully!")
        return redirect('thankyou')

    elif request.method == 'GET':
        address = user.user_address
        phone_number = user.user_phone
        cart_items = CartItem.objects.filter(cart__user=user)
        total_price = sum(item.quantity * item.product.product_price for item in cart_items)

        context = {
            'address': address,
            'phone_number': phone_number,
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, 'checkout.html', context)

# def checkout(request):
#     user = request.user  # Retrieve the current user from the request

#     if request.method == 'POST':
#         cart_items = CartItem.objects.filter(cart__user=user)
#         print("Cart-Items: ", cart_items)
#         total_price = sum(item.quantity * item.product.product_price for item in cart_items)
        

#         # # Create the order
#         # order = Order.objects.create(user=user, total_price=total_price)

#         # # Add cart items to the order
#         # order.items.add(*cart_items)
        
#         # Create the order
#         order = Order.objects.create(user=user, total_price=total_price)
#         print("TYPE OF ORDER: ", type(order))
#         print("TYPE OF ORDER-ITEMS: ", type(order.items))
#         print("ORDER-ITEMS: ", order.items)

#         # Save the order to get an ID assigned
#         # order.save()

#         # Now add each cart item to the order
#         for cart_item in cart_items:
#             print(f"CART ITEM: {cart_item}" )
#             cart_item.save()
#             order.items.add(cart_item)
#             order.save()
            
#         # print("ORDERSSSS -----> ", order.items)
#         print("ORDER ITEMS AFTER ADDING: ", order.items.all())

#         # Clear the user's cart
#         cart_items.delete()

#         messages.success(request, "Order placed successfully!")
#         return redirect('thankyou')

#     elif request.method == 'GET':
        
#         address = user.user_address
#         phone_number = user.user_phone
#         cart_items = CartItem.objects.filter(cart__user=user)
#         total_price = sum(item.quantity * item.product.product_price for item in cart_items)

#         context = {
#             'address': address,
#             'phone_number': phone_number,
#             'cart_items': cart_items,
#             'total_price': total_price,
#         }

#         return render(request, 'checkout.html', context)


#Thankyou
def thankyou(request):
    return render(request, "thankyou.html", {})


@login_required
def view_orders(request):
    # orders = Order.objects.filter(user=request.user)
    print("ORDER OBJECTS:   ", Order.objects.filter())
    orders = Order.objects.filter(user=request.user).select_related('user').prefetch_related('items__product')
    print('ORDERS-----------------: ', orders)
    order_details = []
    for order in orders:
        print(f"ORDERS: {order.items}")
        items = order.items.all()  # Get all items associated with the order
        # item_names = [item.product.product_name for item in items]  # Extract item names
        print(f"ITEMS: {items}")
        item_names = [item.product.product_name for item in items]  # Extract item names
        print(f"Order {order.id} items: {item_names}")  # Debugging line
        order_details.append({'order': order, 'item_names': item_names})
        
    # print("ORDER DETAILS:::::", order_details)
    return render(request, 'view_orders.html', {'order_details': order_details})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, "Order status updated successfully!")
        return redirect('order_detail', order_id=order_id)

    return render(request, 'update_order_status.html', {'order': order})