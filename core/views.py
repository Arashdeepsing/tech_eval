from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login,authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Wishlist,WishlistItem, Order,CartItem, OrderItem
from .forms import SignupForm, LoginForm

from django.contrib import messages




def home(request):
    products = Product.objects.all()  # Adjust according to your needs, e.g., fetching featured products
    return render(request, 'core/home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    return render(request, 'core/cart_detail.html', {'cart_items': cart_items, 'total_price': cart.get_total_price()})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart_detail')


@login_required
def wishlist_detail(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist).select_related('product')
    return render(request, 'core/wishlist_detail.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    return redirect('wishlist_detail')



@login_required
def remove_from_wishlist(request, product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product_id=product_id)
    wishlist_item.delete()
    return redirect('wishlist_detail')



@login_required
def create_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.exists():
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            order.items.add(item)  # Assuming Order model has a related field for items
            item.delete()  # Clear the cart after creating the order
        return redirect('order_detail', order_id=order.id)
    return redirect('cart_detail')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_list.html', {'orders': orders})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == "POST":
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.delete()
        return redirect('order_detail', order_id=order.id)
    return render(request, 'core/checkout.html', {'cart_items': cart_items, 'total_price': cart.get_total_price()})






def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('product_list')  # Redirect to a page after successful login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/login_view.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page or another appropriate page


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
