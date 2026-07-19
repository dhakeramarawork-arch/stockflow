from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Customer
from .forms import CustomerForm
from accounts.models import ActivityLog


@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query)
        )
    customers = customers.order_by('-created_at')
    paginator = Paginator(customers, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'customers/customer_list.html', {
        'page_obj': page_obj, 'query': query,
    })


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='customers',
                description=f'Created customer: {customer.name}',
            )
            messages.success(request, 'Customer created successfully.')
            return redirect('customers:list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {
        'form': form, 'title': 'Add Customer',
    })


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='customers',
                description=f'Updated customer: {customer.name}',
            )
            messages.success(request, 'Customer updated successfully.')
            return redirect('customers:list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {
        'form': form, 'title': 'Edit Customer', 'customer': customer,
    })


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        name = customer.name
        customer.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='customers',
            description=f'Deleted customer: {name}',
        )
        messages.success(request, f'Customer "{name}" deleted.')
        return redirect('customers:list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})