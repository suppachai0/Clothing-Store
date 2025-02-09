from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login_view, name='login'),
]
