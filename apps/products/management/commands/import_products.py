import json
import csv
import os
from django.core.management.base import BaseCommand
from apps.products.models import Product, ProductParameter
from apps.shops.models import Shop, Category

class Command(BaseCommand):
    help = 'Импорт товаров из файлов'
    
    def add_arguments(self, parser):
        parser.add_argument('--shop', type=int, required=True, help='ID магазина')
        parser.add_argument('--file', type=str, required=True, help='Путь к файлу')
    
    def handle(self, *args, **options):
        shop_id = options['shop']
        file_path = options['file']
        
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Магазин с ID {shop_id} не найден'))
            return
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден'))
            return
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.json':
            self.import_from_json(file_path, shop)
        elif ext == '.csv':
            self.import_from_csv(file_path, shop)
        else:
            self.stdout.write(self.style.ERROR('Поддерживаются только .json и .csv файлы'))
    
    def import_from_json(self, file_path, shop):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported = 0
        for item in data:
            category, _ = Category.objects.get_or_create(
                name=item.get('category', 'Общее')
            )
            category.shops.add(shop)
            
            product, created = Product.objects.update_or_create(
                name=item['name'],
                shop=shop,
                defaults={
                    'category': category,
                    'description': item.get('description', ''),
                    'price': item['price'],
                    'quantity': item.get('quantity', 10),
                    'gender': item.get('gender', 'unisex'),
                }
            )
            
            if 'parameters' in item:
                for key, value in item['parameters'].items():
                    ProductParameter.objects.update_or_create(
                        product=product,
                        name=key,
                        defaults={'value': str(value)}
                    )
            
            imported += 1
        
        self.stdout.write(self.style.SUCCESS(f'Импортировано {imported} товаров из {file_path}'))
    
    def import_from_csv(self, file_path, shop):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            imported = 0
            for row in reader:
                category, _ = Category.objects.get_or_create(
                    name=row.get('category', 'Общее')
                )
                category.shops.add(shop)
                
                Product.objects.update_or_create(
                    name=row['name'],
                    shop=shop,
                    defaults={
                        'category': category,
                        'description': row.get('description', ''),
                        'price': float(row['price']),
                        'quantity': int(row.get('quantity', 10)),
                        'gender': row.get('gender', 'unisex'),
                    }
                )
                
                imported += 1
            
            self.stdout.write(self.style.SUCCESS(f'Импортировано {imported} товаров из {file_path}'))