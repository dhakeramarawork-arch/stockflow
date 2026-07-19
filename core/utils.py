"""Shared utility functions used across modules."""
from django.db.models import Sum, F
from datetime import datetime, date
from django.utils import timezone


def generate_sku(prefix='SKU', model_class=None, field='sku'):
    """
    Generate a unique auto-incrementing SKU.
    Format: SKU-YYYYMMDD-XXXX
    """
    today = timezone.now().strftime('%Y%m%d')
    prefix_str = f'{prefix}-{today}-'
    if model_class:
        last = model_class.objects.filter(
            **{f'{field}__startswith': prefix_str}
        ).order_by(f'-{field}').first()
        if last:
            try:
                seq = int(getattr(last, field).split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
    else:
        seq = 1
    return f'{prefix_str}{seq:04d}'


def generate_invoice_number(model_class, prefix='INV'):
    """Generate invoice number: INV-YYYYMMDD-XXXX"""
    return generate_sku(prefix=prefix, model_class=model_class, field='invoice_number')


def generate_purchase_number(model_class, prefix='PUR'):
    """Generate purchase number: PUR-YYYYMMDD-XXXX"""
    return generate_sku(prefix=prefix, model_class=model_class, field='purchase_number')


def get_low_stock_products():
    """Return queryset of products below minimum stock threshold."""
    from products.models import Product
    return Product.objects.filter(
        current_stock__lte=F('minimum_stock'),
        status='active',
    ).exclude(current_stock=0)


def get_out_of_stock_products():
    """Return queryset of products with zero stock."""
    from products.models import Product
    return Product.objects.filter(current_stock=0, status='active')


def get_today_sales():
    """Return total sales amount for today."""
    from sales.models import Sale
    today = date.today()
    return Sale.objects.filter(sale_date__date=today).aggregate(
        total=Sum('total')
    )['total'] or 0


def get_monthly_sales():
    """Return total sales amount for current month."""
    from sales.models import Sale
    now = timezone.now()
    return Sale.objects.filter(
        sale_date__year=now.year,
        sale_date__month=now.month,
    ).aggregate(total=Sum('total'))['total'] or 0