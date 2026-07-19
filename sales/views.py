"""Sales management with automatic stock reduction."""
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .models import Sale, SaleItem
from .forms import SaleForm
from products.models import Product
from accounts.models import ActivityLog
from core.utils import generate_invoice_number


@login_required
def sale_list(request):
    sales = Sale.objects.select_related('customer').order_by('-created_at')
    paginator = Paginator(sales, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'sales/sale_list.html', {'page_obj': page_obj})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


@login_required
@transaction.atomic
def sale_create(request):
    """Create sale with multiple items — auto-reduces product stock."""
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.invoice_number = generate_invoice_number(Sale)
            sale.save()
            product_ids = request.POST.getlist('product[]')
            quantities = request.POST.getlist('quantity[]')
            prices = request.POST.getlist('unit_price[]')
            subtotal = Decimal('0')
            errors = []
            for i, pid in enumerate(product_ids):
                if pid:
                    product = get_object_or_404(Product, pk=pid)
                    qty = Decimal(quantities[i] or '0')
                    price = Decimal(prices[i] or '0')
                    # Check stock availability
                    if product.current_stock < qty:
                        errors.append(f'Insufficient stock for {product.name} '
                                      f'(available: {product.current_stock}, requested: {qty})')
                        continue
                    line_total = qty * price
                    subtotal += line_total
                    SaleItem.objects.create(
                        sale=sale, product=product,
                        quantity=qty, unit_price=price, total=line_total,
                    )
                    # Reduce stock
                    product.current_stock -= qty
                    product.save()
            if errors:
                messages.error(request, ' | '.join(errors))
                # Roll back
                sale.delete()
                return redirect('sales:create')
            sale.subtotal = subtotal
            sale.total = subtotal - sale.discount + sale.tax
            sale.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='sales',
                description=f'Created sale: {sale.invoice_number}',
            )
            messages.success(request, 'Sale recorded and stock updated.')
            return redirect('sales:list')
    else:
        form = SaleForm()
    products = Product.objects.filter(status='active').values(
        'id', 'name', 'sku', 'selling_price', 'current_stock'
    )
    return render(request, 'sales/sale_form.html', {
        'form': form, 'title': 'New Sale', 'products': list(products),
    })


@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        # Restore stock
        for item in sale.items.all():
            product = item.product
            product.current_stock += item.quantity
            product.save()
        invoice = sale.invoice_number
        sale.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='sales',
            description=f'Deleted sale: {invoice}',
        )
        messages.success(request, 'Sale deleted and stock restored.')
        return redirect('sales:list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})