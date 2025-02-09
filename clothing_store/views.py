from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Cart, CartItem
from .forms import CheckoutForm, AddressForm, PaymentForm  # ✅ Import ฟอร์มทั้งหมดที่ต้องใช้

def index(request):
    return render(request, 'index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def payment_success(request):
    return render(request, "payment_success.html")


def cart(request):
    cart_items = []
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
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


def checkout_view(request):
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            # ✅ บันทึกข้อมูลหรือดำเนินการชำระเงิน
            return redirect('payment_success')

    else:
        address_form = AddressForm()
        payment_form = PaymentForm()

    return render(request, "checkout.html", {
        "address_form": address_form,
        "payment_form": payment_form
    })