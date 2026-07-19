"""Inventory management: current stock, movements, adjustments."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product
from .models import StockMovement
from .forms import StockAdjustmentForm
from accounts.models import ActivityLog
from core.utils import get_low_stock_products, get_out_of_stock_products


@login_required
def inventory_overview(request):
    """Current stock overview with low-stock and out-of-stock alerts."""
    products = Product.objects.select_related('category', 'brand', 'unit').filter(status='active')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    low_stock = get_low_stock_products()
    out_stock = get_out_of_stock_products()
    return render(request, 'inventory/overview.html', {
        'page_obj': page_obj,
        'low_stock_products': low_stock,
        'out_of_stock_products': out_stock,
    })


@login_required
def stock_movements(request):
    """Stock movement history."""
    movements = StockMovement.objects.select_related('product').order_by('-created_at')
    paginator = Paginator(movements, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventory/movements.html', {'page_obj': page_obj})


@login_required
def stock_adjustment(request):
    """Manual stock adjustment form."""
    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.reference = 'Manual Adjustment'
            product = movement.product
            # Apply adjustment
            if movement.movement_type in ['damaged', 'expired']:
                product.current_stock -= abs(movement.quantity)
            else:
                product.current_stock += movement.quantity
            product.save()
            movement.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='inventory',
                description=f'Stock adjustment: {product.name} ({movement.movement_type})',
            )
            messages.success(request, 'Stock adjusted successfully.')
            return redirect('inventory:movements')
    else:
        form = StockAdjustmentForm()
    return render(request, 'inventory/adjustment_form.html', {'form': form})