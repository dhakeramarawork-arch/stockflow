"""Purchase management with automatic stock increase."""
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .models import Purchase, PurchaseItem
from .forms import PurchaseForm
from products.models import Product
from accounts.models import ActivityLog
from core.utils import generate_purchase_number


@login_required
def purchase_list(request):
    purchases = Purchase.objects.select_related('supplier').order_by('-created_at')
    paginator = Paginator(purchases, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'purchases/purchase_list.html', {'page_obj': page_obj})


@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    return render(request, 'purchases/purchase_detail.html', {'purchase': purchase})


@login_required
@transaction.atomic
def purchase_create(request):
    """Create purchase with multiple items — auto-increases product stock."""
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.purchase_number = generate_purchase_number(Purchase)
            purchase.save()
            # Process line items
            product_ids = request.POST.getlist('product[]')
            quantities = request.POST.getlist('quantity[]')
            costs = request.POST.getlist('unit_cost[]')
            subtotal = Decimal('0')
            for i, pid in enumerate(product_ids):
                if pid:
                    product = get_object_or_404(Product, pk=pid)
                    qty = Decimal(quantities[i] or '0')
                    cost = Decimal(costs[i] or '0')
                    line_total = qty * cost
                    subtotal += line_total
                    PurchaseItem.objects.create(
                        purchase=purchase, product=product,
                        quantity=qty, unit_cost=cost, total=line_total,
                    )
                    # Increase stock
                    product.current_stock += qty
                    product.save()
            purchase.subtotal = subtotal
            purchase.total = subtotal - purchase.discount + purchase.tax
            purchase.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='purchases',
                description=f'Created purchase: {purchase.purchase_number}',
            )
            messages.success(request, 'Purchase recorded and stock updated.')
            return redirect('purchases:list')
    else:
        form = PurchaseForm()
    products = Product.objects.filter(status='active').values('id', 'name', 'sku', 'purchase_price')
    return render(request, 'purchases/purchase_form.html', {
        'form': form, 'title': 'New Purchase', 'products': list(products),
    })


@login_required
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        # Reverse stock before deleting
        for item in purchase.items.all():
            product = item.product
            product.current_stock -= item.quantity
            product.save()
        purchase_number = purchase.purchase_number
        purchase.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='purchases',
            description=f'Deleted purchase: {purchase_number}',
        )
        messages.success(request, 'Purchase deleted and stock reversed.')
        return redirect('purchases:list')
    return render(request, 'purchases/purchase_confirm_delete.html', {'purchase': purchase})