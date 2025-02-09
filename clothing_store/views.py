from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "เข้าสู่ระบบสำเร็จ!")
            return redirect("index")  # หลังจากเข้าสู่ระบบให้กลับไปหน้าแรก
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, "login.html")

def index(request):
    return render(request, 'index.html')

def product_list(request):
    return render(request, 'product_list.html')

def cart(request):
    return render(request, 'cart.html')

def login_view(request):
    return render(request, 'login.html')
