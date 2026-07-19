"""Product CRUD views with search, filter, pagination, image preview."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Product
from .forms import ProductForm
from accounts.models import ActivityLog
from core.utils import generate_sku


@login_required
def product_list(request):
    """List products with search, category filter, and pagination."""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')

    products = Product.objects.select_related('category', 'brand', 'unit', 'supplier')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(barcode__icontains=query)
        )
    if category:
        products = products.filter(category_id=category)
    if stock_filter == 'low':
        from django.db.models import F
        products = products.filter(current_stock__lte=F('minimum_stock')).exclude(current_stock=0)
    elif stock_filter == 'out':
        products = products.filter(current_stock=0)

    products = products.order_by('-created_at')
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    from categories.models import Category
    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'stock_filter': stock_filter,
        'categories': Category.objects.filter(status='active'),
    })


@login_required
def product_detail(request, pk):
    """Product detail view."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def product_create(request):
    """Create a new product with auto-generated SKU."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.sku = generate_sku(prefix='SKU', model_class=Product, field='sku')
            product.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='products',
                description=f'Created product: {product.name} ({product.sku})',
            )
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('products:list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {
        'form': form, 'title': 'Add Product',
    })


@login_required
def product_update(request, pk):
    """Update existing product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='products',
                description=f'Updated product: {product.name}',
            )
            messages.success(request, 'Product updated successfully.')
            return redirect('products:list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form, 'title': 'Edit Product', 'product': product,
    })


@login_required
def product_delete(request, pk):
    """Delete product with confirmation."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='products',
            description=f'Deleted product: {name}',
        )
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('products:list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})