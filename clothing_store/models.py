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

# 📌 คำสั่งซื้อ (✅ ลบซ้ำ)
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('paid', 'ชำระเงินแล้ว'),
        ('shipped', 'จัดส่งแล้ว'),
        ('completed', 'สำเร็จ'),
        ('cancelled', 'ยกเลิก'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ✅ เปลี่ยนจาก User -> CustomUser
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"

# 📦 รายการสินค้าในคำสั่งซื้อ (✅ ลบซ้ำ)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # ✅ เพิ่ม related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], default="M")
    color = models.CharField(max_length=10, choices=[('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White')], default="black")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size}, {self.color})"

# 🛒 ตะกร้าสินค้า
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # ✅ เปลี่ยนจาก User -> CustomUser
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

# 📦 รายการสินค้าในตะกร้า
class CartItem(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('black', 'Black'),
        ('white', 'White'),
    ]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, default="M")
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="black")

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size}, {self.color})"
