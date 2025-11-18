from rest_framework import serializers
from .models import Category, Product, CartItem, Order, OrderItem
from django.contrib.auth.models import User


# === Сериализатор категории ===
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# === Сериализатор товара (для чтения) ===
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'description', 
                  'old_price', 'new_price', 'image']
    
    def to_representation(self, instance):
        """Для совместимости с фронтом"""
        data = super().to_representation(instance)
        # Добавляем category как строку для фронта
        data['category'] = instance.category.name.lower()
        return data


# === Сериализатор товара (для создания/обновления) ===
class ProductCreateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'description', 
                  'old_price', 'new_price', 'image']
    
    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        
        # Если передано имя категории, найти или создать категорию
        if category_name and 'category' not in validated_data:
            category, _ = Category.objects.get_or_create(
                name=category_name.capitalize()
            )
            validated_data['category'] = category
        
        return super().create(validated_data)


# === Сериализатор пользователя ===
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# === Сериализатор элемента корзины ===
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'subtotal']
        read_only_fields = ['user', 'subtotal']
    
    def create(self, validated_data):
        # Автоматически привязываем к текущему пользователю
        user = self.context['request'].user
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        
        # Проверяем, есть ли уже такой товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': validated_data.get('quantity', 1)}
        )
        
        if not created:
            # Если товар уже в корзине, увеличиваем количество
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
        
        return cart_item


# === Сериализатор элемента заказа ===
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'subtotal']
        read_only_fields = ['order', 'subtotal']


# === Сериализатор заказа ===
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total', 'status', 'order_items']
        read_only_fields = ['user', 'created_at', 'total']


# === Сериализатор создания заказа ===
class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # Создаем заказ
        order = Order.objects.create(user=user, **validated_data)
        
        # Копируем товары из корзины в заказ
        cart_items = CartItem.objects.filter(user=user)
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        
        # Подсчитываем итоговую сумму
        order.calculate_total()
        
        # Очищаем корзину
        cart_items.delete()
        
        return order


# === Сериализатор регистрации ===
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


# === Сериализатор логина ===
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)