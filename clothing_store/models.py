from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username

# 🛍️ สินค้า
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

# 🛒 คำสั่งซื้อ
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('paid', 'ชำระเงินแล้ว'),
        ('shipped', 'จัดส่งแล้ว'),
        ('completed', 'สำเร็จ'),
        ('cancelled', 'ยกเลิก'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default="ไม่ระบุ")  # ✅ กำหนดค่าเริ่มต้น
    phone_number = models.CharField(max_length=10, default="0000000000")  # ✅ กำหนดค่าเริ่มต้น
    address = models.TextField(default="ไม่ระบุ")  # ✅ กำหนดค่าเริ่มต้น
    postal_code = models.CharField(max_length=5, default="00000")  # ✅ กำหนดค่าเริ่มต้น
    payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'บัตรเครดิต'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'โอนเงินผ่านธนาคาร'),
        ('cash_on_delivery', 'เก็บเงินปลายทาง')
    ], default="cash_on_delivery")  # ✅ กำหนดค่าเริ่มต้น
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"


# 📦 รายการสินค้าในคำสั่งซื้อ
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, choices=[
        ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')
    ], default="M")
    color = models.CharField(max_length=10, choices=[
        ('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White')
    ], default="black")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size}, {self.color})"

# 🛒 ตะกร้าสินค้า
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

# 📦 รายการสินค้าในตะกร้า
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, choices=[
        ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')
    ], default="M")
    color = models.CharField(max_length=10, choices=[
        ('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White')
    ], default="black")

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size}, {self.color})"
