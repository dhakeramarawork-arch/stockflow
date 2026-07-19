"""Category CRUD views with search, pagination, and activity logging."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Category
from .forms import CategoryForm
from accounts.models import ActivityLog


@login_required
def category_list(request):
    """List categories with search and pagination."""
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    categories = Category.objects.all()
    if query:
        categories = categories.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if status:
        categories = categories.filter(status=status)

    categories = categories.order_by('-created_at')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'categories/category_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status': status,
    })


@login_required
def category_create(request):
    """Create a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='categories',
                description=f'Created category: {category.name}',
            )
            messages.success(request, 'Category created successfully.')
            return redirect('categories:list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {
        'form': form, 'title': 'Add Category',
    })


@login_required
def category_update(request, pk):
    """Update an existing category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='categories',
                description=f'Updated category: {category.name}',
            )
            messages.success(request, 'Category updated successfully.')
            return redirect('categories:list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {
        'form': form, 'title': 'Edit Category', 'category': category,
    })


@login_required
def category_delete(request, pk):
    """Delete a category with confirmation."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='categories',
            description=f'Deleted category: {name}',
        )
        messages.success(request, f'Category "{name}" deleted successfully.')
        return redirect('categories:list')
    return render(request, 'categories/category_confirm_delete.html', {
        'category': category,
    })