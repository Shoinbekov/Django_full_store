from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductCreateSerializer,
    CartItemSerializer, 
    OrderSerializer,
    OrderCreateSerializer,
    RegisterSerializer,
    LoginSerializer
)


# === Категории ===
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# === Товары ===
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__name']
    search_fields = ['name', 'description']
    ordering_fields = ['new_price', 'name', 'id']
    ordering = ['id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_name = request.query_params.get('category', '').lower()
        if not category_name:
            return Response(
                {'error': 'Category parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            category = Category.objects.get(name__iexact=category_name)
            products = Product.objects.filter(category=category)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        products = Product.objects.all()[:4]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_collections(self, request):
        products = Product.objects.all().order_by('-id')[:8]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# === Корзина ===
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    # 🚨 РЕКОМЕНДУЕТСЯ: В продакшене используйте IsAuthenticated
    permission_classes = [AllowAny] 
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(user=self.request.user).select_related('product', 'product__category')
        return CartItem.objects.none()
    
    # 🚨 ИСПРАВЛЕНИЕ: Добавляем action для /api/cart/add_item/
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Добавляет или увеличивает количество товара в корзине"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 🚨 ИСПРАВЛЕНИЕ: Добавляем action для /api/cart/remove_item/
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Уменьшает количество товара в корзине или удаляет его"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        product_id = request.data.get('product_id')
        
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def total(self, request):
        if not request.user.is_authenticated:
            return Response({
                'total': 0,
                'count': 0,
                'message': 'User not authenticated'
            })
        
        cart_items = self.get_queryset()
        total = sum(item.subtotal() for item in cart_items)
        count = sum(item.quantity for item in cart_items)
        
        return Response({
            'total': total,
            'count': count
        })
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        self.get_queryset().delete()
        return Response({'message': 'Cart cleared successfully'})
    
    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        cart_item = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)


# === Заказы ===
class OrderViewSet(viewsets.ModelViewSet):
    # ... (Остальной код OrderViewSet без изменений)
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user).prefetch_related('order_items__product')
        return Order.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'results': [],
                'message': 'User not authenticated'
            })
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        order = self.get_object()
        
        if order.status == 'Delivered':
            return Response(
                {'error': 'Cannot cancel delivered order'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'Cancelled'
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)


# === Аутентификация ===
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'error': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'User was not authenticated'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_auth(request):
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        })
    
    return Response({
        'authenticated': False
    })