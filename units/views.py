from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Unit
from .forms import UnitForm
from accounts.models import ActivityLog


@login_required
def unit_list(request):
    query = request.GET.get('q', '')
    units = Unit.objects.all()
    if query:
        units = units.filter(Q(name__icontains=query) | Q(short_code__icontains=query))
    units = units.order_by('-created_at')
    paginator = Paginator(units, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'units/unit_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='units',
                description=f'Created unit: {unit.name}',
            )
            messages.success(request, 'Unit created successfully.')
            return redirect('units:list')
    else:
        form = UnitForm()
    return render(request, 'units/unit_form.html', {'form': form, 'title': 'Add Unit'})


@login_required
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='units',
                description=f'Updated unit: {unit.name}',
            )
            messages.success(request, 'Unit updated successfully.')
            return redirect('units:list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'units/unit_form.html', {
        'form': form, 'title': 'Edit Unit', 'unit': unit,
    })


@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        name = unit.name
        unit.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='units',
            description=f'Deleted unit: {name}',
        )
        messages.success(request, f'Unit "{name}" deleted.')
        return redirect('units:list')
    return render(request, 'units/unit_confirm_delete.html', {'unit': unit})