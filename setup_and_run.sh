#!/bin/bash
# ============================================================
# StockFlow Inventory System — Setup & Run Script
# ============================================================

set -e

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗃️  Running migrations..."
python manage.py makemigrations accounts categories brands units products suppliers customers purchases sales inventory
python manage.py migrate

echo "👤 Creating superuser (if not exists)..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
import os
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin / admin123')
else:
    print('ℹ️  Superuser already exists')
EOF

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🌱 Loading sample data..."
python manage.py shell <<EOF
from categories.models import Category
from brands.models import Brand
from units.models import Unit
from suppliers.models import Supplier
from customers.models import Customer

if not Category.objects.exists():
    for name in ['Electronics', 'Clothing', 'Food & Beverage', 'Furniture', 'Stationery']:
        Category.objects.create(name=name, description=f'{name} category')
    print('✅ Sample categories created')

if not Brand.objects.exists():
    for name in ['Samsung', 'Apple', 'Sony', 'Nike', 'Generic']:
        Brand.objects.create(name=name)
    print('✅ Sample brands created')

if not Unit.objects.exists():
    for name, code in [('Piece','pc'), ('Box','box'), ('Pack','pack'), ('Kg','kg'), ('Litre','ltr'), ('Meter','m')]:
        Unit.objects.create(name=name, short_code=code)
    print('✅ Sample units created')

if not Supplier.objects.exists():
    Supplier.objects.create(company_name='Global Supplies Ltd', contact_person='John Doe',
                            phone='+1234567890', email='john@globalsupplies.com',
                            city='New York', country='USA')
    print('✅ Sample supplier created')

if not Customer.objects.exists():
    Customer.objects.create(name='Walk-in Customer', phone='000-000-0000')
    print('✅ Sample customer created')
EOF

echo ""
echo "============================================================"
echo "✅ Setup complete!"
echo "============================================================"
echo "🔑 Admin Login:  username=admin  password=admin123"
echo "🌐 Starting server at http://127.0.0.1:8000/"
echo "============================================================"
echo ""

python manage.py runserver