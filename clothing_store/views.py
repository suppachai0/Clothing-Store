from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CustomUser, Product, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm, CustomUserCreationForm

def index(request):
    return render(request, 'index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def payment_success(request):
    return render(request, "payment_success.html")

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        size = request.POST.get("size", "M")
        color = request.POST.get("color", "black")

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"✅ เพิ่ม {product.name} ลงในตะกร้าสำเร็จ!")

    return redirect('cart')

@login_required
def checkout_view(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["fullname"]
            phone_number = form.cleaned_data["phone_number"]
            address = form.cleaned_data["address"]
            postal_code = form.cleaned_data["postal_code"]
            payment_method = form.cleaned_data["payment_method"]

            cart = get_object_or_404(Cart, user=request.user)

            if not cart.items.exists():
                messages.warning(request, "⚠️ ตะกร้าของคุณว่างเปล่า ไม่สามารถสั่งซื้อได้")
                return redirect("cart")

            total_price = sum(item.product.price * item.quantity for item in cart.items.all())

            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone_number=phone_number,
                address=address,
                postal_code=postal_code,
                payment_method=payment_method,
                total_price=total_price
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    color=item.color
                )

            cart.items.all().delete()

            messages.success(request, "🎉 คำสั่งซื้อของคุณถูกบันทึกเรียบร้อยแล้ว!")
            return redirect("payment_success")
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"form": form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()

    return render(request, 'order_detail.html', {
        'order': order,
        'order_items': order_items,
        'user_id': order.user.id
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    messages.success(request, f"🛒 ลบสินค้า {cart_item.product.name} ออกจากตะกร้าสำเร็จ!")
    cart_item.delete()
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        new_quantity = request.POST.get("quantity", 1)
        if int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, "🛒 สินค้าถูกลบออกจากตะกร้าเนื่องจากจำนวนเป็น 0")

    return redirect('cart')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"🎉 สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ {user.username}")
            return redirect('index')
        else:
            messages.error(request, "❌ กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"🔓 เข้าสู่ระบบสำเร็จ! ยินดีต้อนรับ {user.username}")
            return redirect('index')
        else:
            messages.error(request, "❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "📢 ออกจากระบบเรียบร้อยแล้ว")
    return redirect('index')
