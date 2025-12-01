from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from decimal import Decimal

from gunicorn.config import User

from .models import Category, Product, CartItem, Order, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class Cart:
    pass


@admin.register(Cart)
class CartItem(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_editable = ('quantity',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    list_filter = ('created_at', 'user')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'method', 'status')
    list_filter = ('status', 'method')








