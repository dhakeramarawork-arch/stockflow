"""Reports: sales, purchases, inventory, profit, low-stock, with CSV export."""
import csv
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.http import HttpResponse
from django.shortcuts import render

from products.models import Product
from suppliers.models import Supplier
from customers.models import Customer
from purchases.models import Purchase
from sales.models import Sale
from core.utils import get_low_stock_products


def _csv_response(filename, header, rows):
    """Helper to build a CSV download response."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    return response


@login_required
def reports_index(request):
    """Reports landing page."""
    return render(request, 'reports/index.html')


@login_required
def sales_report(request):
    """Sales report with optional CSV export."""
    sales = Sale.objects.select_related('customer').order_by('-sale_date')
    total = sales.aggregate(t=Sum('total'))['t'] or 0
    if request.GET.get('export') == 'csv':
        rows = [(s.invoice_number, s.customer.name if s.customer else '',
                 s.sale_date, s.total, s.payment_status) for s in sales]
        return _csv_response('sales_report.csv',
                              ['Invoice', 'Customer', 'Date', 'Total', 'Status'], rows)
    return render(request, 'reports/sales_report.html', {
        'sales': sales[:100], 'total': total, 'count': sales.count(),
    })


@login_required
def purchase_report(request):
    purchases = Purchase.objects.select_related('supplier').order_by('-purchase_date')
    total = purchases.aggregate(t=Sum('total'))['t'] or 0
    if request.GET.get('export') == 'csv':
        rows = [(p.purchase_number, p.supplier.company_name if p.supplier else '',
                 p.purchase_date, p.total, p.payment_status) for p in purchases]
        return _csv_response('purchase_report.csv',
                              ['Purchase #', 'Supplier', 'Date', 'Total', 'Status'], rows)
    return render(request, 'reports/purchase_report.html', {
        'purchases': purchases[:100], 'total': total, 'count': purchases.count(),
    })


@login_required
def inventory_report(request):
    products = Product.objects.select_related('category', 'brand').filter(status='active')
    total_value = sum(p.stock_value for p in products)
    if request.GET.get('export') == 'csv':
        rows = [(p.sku, p.name, p.category.name if p.category else '',
                 p.current_stock, p.minimum_stock, p.purchase_price, p.stock_value)
                for p in products]
        return _csv_response('inventory_report.csv',
                              ['SKU', 'Name', 'Category', 'Stock', 'Min Stock',
                               'Purchase Price', 'Stock Value'], rows)
    return render(request, 'reports/inventory_report.html', {
        'products': products, 'total_value': total_value,
    })


@login_required
def profit_report(request):
    """Profit report based on sales vs purchase cost."""
    sales = Sale.objects.prefetch_related('items__product').order_by('-sale_date')
    profit_data = []
    total_profit = 0
    for sale in sales:
        sale_profit = 0
        for item in sale.items.all():
            cost = item.product.purchase_price * item.quantity
            revenue = item.unit_price * item.quantity
            sale_profit += (revenue - cost)
        profit_data.append({'sale': sale, 'profit': sale_profit})
        total_profit += sale_profit
    return render(request, 'reports/profit_report.html', {
        'profit_data': profit_data[:100], 'total_profit': total_profit,
    })


@login_required
def low_stock_report(request):
    products = get_low_stock_products()
    if request.GET.get('export') == 'csv':
        rows = [(p.sku, p.name, p.current_stock, p.minimum_stock, p.maximum_stock)
                for p in products]
        return _csv_response('low_stock_report.csv',
                              ['SKU', 'Name', 'Current Stock', 'Min', 'Max'], rows)
    return render(request, 'reports/low_stock_report.html', {'products': products})


@login_required
def supplier_report(request):
    suppliers = Supplier.objects.annotate(
        purchase_count=Count('purchases'),
        total_purchase=Sum('purchases__total'),
    )
    return render(request, 'reports/supplier_report.html', {'suppliers': suppliers})


@login_required
def customer_report(request):
    customers = Customer.objects.annotate(
        sale_count=Count('sales'),
        total_sale=Sum('sales__total'),
    )
    return render(request, 'reports/customer_report.html', {'customers': customers})