from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Supplier
from .forms import SupplierForm
from accounts.models import ActivityLog


@login_required
def supplier_list(request):
    query = request.GET.get('q', '')
    suppliers = Supplier.objects.all()
    if query:
        suppliers = suppliers.filter(
            Q(company_name__icontains=query) |
            Q(contact_person__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    suppliers = suppliers.order_by('-created_at')
    paginator = Paginator(suppliers, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'suppliers/supplier_list.html', {
        'page_obj': page_obj, 'query': query,
    })


@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='suppliers',
                description=f'Created supplier: {supplier.company_name}',
            )
            messages.success(request, 'Supplier created successfully.')
            return redirect('suppliers:list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {
        'form': form, 'title': 'Add Supplier',
    })


@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='suppliers',
                description=f'Updated supplier: {supplier.company_name}',
            )
            messages.success(request, 'Supplier updated successfully.')
            return redirect('suppliers:list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {
        'form': form, 'title': 'Edit Supplier', 'supplier': supplier,
    })


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        name = supplier.company_name
        supplier.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='suppliers',
            description=f'Deleted supplier: {name}',
        )
        messages.success(request, f'Supplier "{name}" deleted.')
        return redirect('suppliers:list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})