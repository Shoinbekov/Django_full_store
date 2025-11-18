from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from decimal import Decimal
from .models import Category, Product, CartItem, Order, OrderItem


# === Вспомогательная функция для форматирования валюты ===
# Возвращает простую строку (str), что предотвращает ошибку SafeString
def format_currency(value):
    """Форматирует Decimal/float в строку X.XX."""
    if value is None:
        return "0.00"
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "0.00"

# ---

# === Inline для OrderItem ===
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal_inline_display',) 
    fields = ('product', 'quantity', 'subtotal_inline_display')
    
    def subtotal_inline_display(self, obj):
        if obj.pk:
            return f"${format_currency(obj.subtotal())}"
        return "-"
    subtotal_inline_display.short_description = 'Subtotal'

# ---

# === Category Admin ===
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count', 'total_value')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'
    
    def total_value(self, obj):
        total = obj.products.aggregate(total=Sum('new_price'))['total']
        if total is None:
            total = Decimal('0.00')
        return f"${format_currency(total)}" 
    total_value.short_description = 'Total Value'

# ---

# === Product Admin ===
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 'new_price' используется для list_editable
    list_display = ('id', 'name', 'category', 'new_price', 'old_price_display', 
                    'discount_percent', 'image_preview') 
    list_filter = ('category', 'new_price')
    search_fields = ('name', 'description')
    list_editable = ('new_price',) 
    list_per_page = 20
    ordering = ('id',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('old_price', 'new_price'),
            'classes': ('wide',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    actions = ['apply_discount_10', 'apply_discount_20', 'apply_discount_50']
    
    def old_price_display(self, obj):
        return format_html(
            '<span style="color: #999; text-decoration: line-through;">${}</span>',
            format_currency(obj.old_price)
        )
    old_price_display.short_description = 'Old Price'
    
    def discount_percent(self, obj):
        if obj.old_price and obj.old_price > 0:
            discount = ((obj.old_price - obj.new_price) / obj.old_price) * 100
            color = '#FF5722' if discount > 30 else '#FF9800'
            
            # ИСПРАВЛЕНИЕ: Форматируем числовое значение в строку ДО передачи в format_html
            discount_str = f"{float(discount):.0f}"
            
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px;">-{}%</span>',
                color, discount_str
            )
        return '-'
    discount_percent.short_description = 'Discount'
    
    def image_preview(self, obj):
        if obj.image:
            image_url = getattr(obj.image, 'url', obj.image)
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                image_url
            )
        return '-'
    image_preview.short_description = 'Image'
    
    # === Actions (ИСПРАВЛЕННЫЕ ОПИСАНИЯ для предотвращения TypeError: %d format) ===
    @admin.action(description='Apply 10%% discount to selected products')
    def apply_discount_10(self, request, queryset):
        for product in queryset:
            product.new_price = product.old_price * Decimal('0.9')
            product.save()
        self.message_user(request, f'{queryset.count()} products updated with 10% discount')
    
    @admin.action(description='Apply 20%% discount to selected products')
    def apply_discount_20(self, request, queryset):
        for product in queryset:
            product.new_price = product.old_price * Decimal('0.8')
            product.save()
        self.message_user(request, f'{queryset.count()} products updated with 20% discount')
    
    @admin.action(description='Apply 50%% discount to selected products')
    def apply_discount_50(self, request, queryset):
        for product in queryset:
            product.new_price = product.old_price * Decimal('0.5')
            product.save()
        self.message_user(request, f'{queryset.count()} products updated with 50% discount')

# ---

# === CartItem Admin ===
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'subtotal_display')
    list_filter = ('user',)
    search_fields = ('product__name', 'user__username')
    
    def subtotal_display(self, obj):
        subtotal = obj.product.new_price * obj.quantity
        return f"${format_currency(subtotal)}"
    subtotal_display.short_description = 'Subtotal'

# ---

# === Order Admin ===
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_display', 'total_display', 'items_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    list_per_page = 20
    readonly_fields = ('created_at', 'total_display', 'items_count')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'created_at')
        }),
        ('Financial Details', {
            'fields': ('total_display', 'items_count'),
            'classes': ('wide',)
        }),
    )
    
    actions = ['mark_as_pending', 'mark_as_processing', 'mark_as_delivered', 'mark_as_cancelled']
    
    def status_display(self, obj):
        colors = {
            'Pending': '#FF9800',
            'Processing': '#2196F3',
            'Delivered': '#4CAF50',
            'Cancelled': '#F44336'
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            color, obj.status
        )
    status_display.short_description = 'Status'
    
    def total_display(self, obj):
        return format_html(
            '<span style="color: #4CAF50; font-size: 16px; font-weight: bold;">${}</span>',
            format_currency(obj.total)
        )
    total_display.short_description = 'Total Amount'
    
    def items_count(self, obj):
        count = obj.order_items.count()
        return format_html(
            '<span style="background-color: #2196F3; color: white; padding: 3px 10px; border-radius: 3px;">{} items</span>',
            count
        )
    items_count.short_description = 'Items'
    
    # === Actions ===
    @admin.action(description='Mark as Pending')
    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')
        self.message_user(request, f'{queryset.count()} orders marked as Pending')
    
    @admin.action(description='Mark as Processing')
    def mark_as_processing(self, request, queryset):
        queryset.update(status='Processing')
        self.message_user(request, f'{queryset.count()} orders marked as Processing')
    
    @admin.action(description='Mark as Delivered')
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
        self.message_user(request, f'{queryset.count()} orders marked as Delivered')
    
    @admin.action(description='Mark as Cancelled')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, f'{queryset.count()} orders marked as Cancelled')

# ---

# === OrderItem Admin ===
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal_display')
    list_filter = ('order__status', 'product__category')
    search_fields = ('product__name', 'order__user__username')
    list_per_page = 20
    readonly_fields = ('subtotal_display',)
    
    def subtotal_display(self, obj):
        return format_html(
            '<strong>${}</strong>', 
            format_currency(obj.subtotal())
        )
    subtotal_display.short_description = 'Subtotal'