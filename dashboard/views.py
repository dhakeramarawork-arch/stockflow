"""Custom dashboard view (NOT Django admin)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import date, timedelta

from categories.models import Category
from brands.models import Brand
from products.models import Product
from suppliers.models import Supplier
from customers.models import Customer
from purchases.models import Purchase
from sales.models import Sale
from accounts.models import ActivityLog
from core.utils import get_low_stock_products, get_out_of_stock_products


@login_required
def dashboard_home(request):
    """
    Main dashboard with KPIs, charts, recent activity, and quick actions.
    """
    today = date.today()
    now = timezone.now()

    # KPI counts
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_brands = Brand.objects.count()
    total_suppliers = Supplier.objects.count()
    total_customers = Customer.objects.count()
    low_stock = get_low_stock_products().count()
    out_of_stock = get_out_of_stock_products().count()

    # Sales metrics
    today_sales = Sale.objects.filter(sale_date__date=today).aggregate(
        total=Sum('total')
    )['total'] or 0
    month_sales = Sale.objects.filter(
        sale_date__year=now.year, sale_date__month=now.month
    ).aggregate(total=Sum('total'))['total'] or 0

    # Recent activity
    recent_activities = ActivityLog.objects.select_related('user')[:8]

    # Recent transactions
    recent_sales = Sale.objects.select_related('customer')[:5]
    recent_purchases = Purchase.objects.select_related('supplier')[:5]

    # Sales chart data — last 7 days
    sales_labels = []
    sales_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        sales_labels.append(d.strftime('%a'))
        total = Sale.objects.filter(sale_date__date=d).aggregate(
            total=Sum('total')
        )['total'] or 0
        sales_data.append(float(total))

    # Category distribution
    category_labels = []
    category_data = []
    for cat in Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)[:6]:
        category_labels.append(cat.name)
        category_data.append(cat.product_count)

    # Stock status for donut chart
    in_stock = Product.objects.filter(
        current_stock__gt=F('minimum_stock'), status='active'
    ).count()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_brands': total_brands,
        'total_suppliers': total_suppliers,
        'total_customers': total_customers,
        'low_stock_count': low_stock,
        'out_of_stock_count': out_of_stock,
        'today_sales': today_sales,
        'month_sales': month_sales,
        'recent_activities': recent_activities,
        'recent_sales': recent_sales,
        'recent_purchases': recent_purchases,
        'sales_labels': sales_labels,
        'sales_data': sales_data,
        'category_labels': category_labels,
        'category_data': category_data,
        'in_stock_count': in_stock,
    }
    return render(request, 'dashboard/dashboard.html', context)