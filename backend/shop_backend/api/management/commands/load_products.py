"""
Management команда для загрузки товаров в БД

Создайте структуру папок:
api/
  management/
    __init__.py
    commands/
      __init__.py
      load_products.py  <-- этот файл

Запуск: python manage.py load_products
"""

from django.core.management.base import BaseCommand
from api.models import Category, Product


class Command(BaseCommand):
    help = 'Load products into database'

    def handle(self, *args, **kwargs):
        # Создаем категории
        women_cat, _ = Category.objects.get_or_create(
            name='women',
            defaults={'description': 'Women\'s clothing and accessories'}
        )
        men_cat, _ = Category.objects.get_or_create(
            name='men',
            defaults={'description': 'Men\'s clothing and accessories'}
        )
        kid_cat, _ = Category.objects.get_or_create(
            name='kid',
            defaults={'description': 'Kids\' clothing and accessories'}
        )

        # Список товаров (соответствует all_product.js)
        products_data = [
            # Women's products (1-12)
            {
                'id': 1,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 50.0,
                'old_price': 80.5,
                'image': 'http://localhost:3000/images/product_1.png',
                'description': 'Elegant striped blouse with flutter sleeves'
            },
            {
                'id': 2,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_2.png',
                'description': 'Stylish blouse with peplum hem'
            },
            {
                'id': 3,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 60.0,
                'old_price': 100.5,
                'image': 'http://localhost:3000/images/product_3.png',
                'description': 'Comfortable and fashionable blouse'
            },
            {
                'id': 4,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 100.0,
                'old_price': 150.0,
                'image': 'http://localhost:3000/images/product_4.png',
                'description': 'Premium quality blouse'
            },
            {
                'id': 5,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_5.png',
                'description': 'Elegant design for any occasion'
            },
            {
                'id': 6,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_6.png',
                'description': 'Modern style blouse'
            },
            {
                'id': 7,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_7.png',
                'description': 'Trendy overlap collar design'
            },
            {
                'id': 8,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_8.png',
                'description': 'Perfect for office wear'
            },
            {
                'id': 9,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_9.png',
                'description': 'Casual yet elegant'
            },
            {
                'id': 10,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_10.png',
                'description': 'Versatile wardrobe essential'
            },
            {
                'id': 11,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_11.png',
                'description': 'Comfortable fit all day'
            },
            {
                'id': 12,
                'name': 'Striped Flutter Sleeve Overlap Collar Peplum Hem Blouse',
                'category': women_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_12.png',
                'description': 'Beautiful striped pattern'
            },

            # Men's products (13-24)
            {
                'id': 13,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_13.png',
                'description': 'Stylish bomber jacket for men'
            },
            {
                'id': 14,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_14.png',
                'description': 'Slim fit design'
            },
            {
                'id': 15,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_15.png',
                'description': 'Perfect for casual outings'
            },
            {
                'id': 16,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_16.png',
                'description': 'Comfortable and stylish'
            },
            {
                'id': 17,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_17.png',
                'description': 'Durable material'
            },
            {
                'id': 18,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_18.png',
                'description': 'Modern fit bomber'
            },
            {
                'id': 19,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_19.png',
                'description': 'Trendy green color'
            },
            {
                'id': 20,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_20.png',
                'description': 'Versatile jacket'
            },
            {
                'id': 21,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_21.png',
                'description': 'Full-zip convenience'
            },
            {
                'id': 22,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_22.png',
                'description': 'Premium quality fabric'
            },
            {
                'id': 23,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_23.png',
                'description': 'Contemporary style'
            },
            {
                'id': 24,
                'name': 'Men Green Solid Zippered Full-Zip Slim Fit Bomber Jacket',
                'category': men_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_24.png',
                'description': 'Essential wardrobe piece'
            },

            # Kids' products (25-36)
            {
                'id': 25,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_25.png',
                'description': 'Fun and colorful sweatshirt'
            },
            {
                'id': 26,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_26.png',
                'description': 'Comfortable hooded design'
            },
            {
                'id': 27,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_27.png',
                'description': 'Perfect for active kids'
            },
            {
                'id': 28,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_28.png',
                'description': 'Vibrant orange color'
            },
            {
                'id': 29,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_29.png',
                'description': 'Soft and warm'
            },
            {
                'id': 30,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_30.png',
                'description': 'Durable for playtime'
            },
            {
                'id': 31,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_31.png',
                'description': 'Trendy colorblocked style'
            },
            {
                'id': 32,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_32.png',
                'description': 'Cozy and comfortable'
            },
            {
                'id': 33,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_33.png',
                'description': 'Easy to wear'
            },
            {
                'id': 34,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_34.png',
                'description': 'Machine washable'
            },
            {
                'id': 35,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_35.png',
                'description': 'Perfect for everyday wear'
            },
            {
                'id': 36,
                'name': 'Boys Orange Colourblocked Hooded Sweatshirt',
                'category': kid_cat,
                'new_price': 85.0,
                'old_price': 120.5,
                'image': 'http://localhost:3000/images/product_36.png',
                'description': 'Kids favorite sweatshirt'
            },
        ]

        # Удаляем старые товары (опционально)
        Product.objects.all().delete()

        # Загружаем товары
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created: {product.name} (ID: {product.id})')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully loaded {created_count} products!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total products in DB: {Product.objects.count()}')
        )