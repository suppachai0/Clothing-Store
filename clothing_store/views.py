from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages  # ✅ ใช้สำหรับแจ้งเตือน
from .models import Product, Cart, CartItem, Order, OrderItem
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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')  # ✅ รับค่าอีเมลจากฟอร์ม
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]  # ✅ บันทึกอีเมล
            user.save()
            login(request, user)
            messages.success(request, f"🎉 สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ {user.username}")
            return redirect('index')
        else:
            messages.error(request, "❌ กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
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
            messages.success(request, f"🔓 เข้าสู่ระบบสำเร็จ! ยินดีต้อนรับ {user.username}")
            return redirect('index')
        else:
            messages.error(request, "❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "📢 ออกจากระบบเรียบร้อยแล้ว")
    return redirect('index')

@login_required
def checkout_view(request):
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            order = create_order(request.user)
            messages.success(request, "🛒 คำสั่งซื้อถูกสร้างเรียบร้อยแล้ว!")
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
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    print(f"🛒 คำสั่งซื้อ {order.id} มีสินค้า: {order_items.count()} รายการ")
    for item in order_items:
        print(f"➡️ {item.product.name}, จำนวน: {item.quantity}, ขนาด: {item.size}, สี: {item.color}")

    return render(request, 'order_detail.html', {
        'order': order,
        'order_items': order_items,
        'user_id': order.user.id  # ✅ ส่ง user_id ไปยัง template
    })

def create_order(user):
    cart = get_object_or_404(Cart, user=user)

    if not cart.items.exists():
        messages.warning(user, "⚠️ ตะกร้าว่างเปล่า ไม่สามารถสร้างคำสั่งซื้อได้")
        return None

    last_order = Order.objects.filter(user=user).order_by('-created_at').first()
    if last_order and not last_order.orderitem_set.exists():
        print(f"⚠️ คำสั่งซื้อ #{last_order.id} ยังไม่มีสินค้า ลบออกก่อน")
        last_order.delete()

    order = Order.objects.create(user=user, total_price=0)
    print(f"📝 สร้างคำสั่งซื้อใหม่ ID: {order.id}")

    total_price = 0
    for item in cart.items.all():
        order_item = OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            size=item.size,
            color=item.color
        )
        print(f"✅ บันทึก OrderItem: {order_item.id}")

        total_price += item.product.price * item.quantity

    order.total_price = total_price
    order.save()
    print(f"💰 คำสั่งซื้อ {order.id} รวมเป็นเงิน: {order.total_price} บาท")

    cart.items.all().delete()
    print("🧹 ล้างตะกร้าสำเร็จ")

    return order

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
