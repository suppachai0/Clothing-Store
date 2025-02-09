from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Cart, CartItem, Order, OrderItem  # ✅ Import OrderItem ด้วย
from .forms import CheckoutForm, AddressForm, PaymentForm

def index(request):
    return render(request, 'index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def payment_success(request):
    return render(request, "payment_success.html")

@login_required
def cart(request):
    cart_items = []
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def checkout_view(request):
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            order = create_order(request.user)
            return redirect('payment_success')

    else:
        address_form = AddressForm()
        payment_form = PaymentForm()

    return render(request, "checkout.html", {
        "address_form": address_form,
        "payment_form": payment_form
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # ✅ ตรวจสอบว่า `Order` มี `user` field
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def create_order(user):
    """ ฟังก์ชันสำหรับสร้างคำสั่งซื้อ """
    cart = get_object_or_404(Cart, user=user)
    order = Order.objects.create(user=user, total_price=0)

    total_price = 0
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        total_price += item.product.price * item.quantity

    order.total_price = total_price
    order.save()

    # เคลียร์ตะกร้าหลังจากสั่งซื้อ
    cart.items.all().delete()

    return order
