"""Brand CRUD views."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Brand
from .forms import BrandForm
from accounts.models import ActivityLog


@login_required
def brand_list(request):
    query = request.GET.get('q', '')
    brands = Brand.objects.all()
    if query:
        brands = brands.filter(Q(name__icontains=query) | Q(description__icontains=query))
    brands = brands.order_by('-created_at')
    paginator = Paginator(brands, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'brands/brand_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='brands',
                description=f'Created brand: {brand.name}',
            )
            messages.success(request, 'Brand created successfully.')
            return redirect('brands:list')
    else:
        form = BrandForm()
    return render(request, 'brands/brand_form.html', {'form': form, 'title': 'Add Brand'})


@login_required
def brand_update(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='brands',
                description=f'Updated brand: {brand.name}',
            )
            messages.success(request, 'Brand updated successfully.')
            return redirect('brands:list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'brands/brand_form.html', {
        'form': form, 'title': 'Edit Brand', 'brand': brand,
    })


@login_required
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        name = brand.name
        brand.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='brands',
            description=f'Deleted brand: {name}',
        )
        messages.success(request, f'Brand "{name}" deleted.')
        return redirect('brands:list')
    return render(request, 'brands/brand_confirm_delete.html', {'brand': brand})