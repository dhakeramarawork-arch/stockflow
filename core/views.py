"""Core views: landing page, error handlers."""
from django.shortcuts import render, redirect


def home(request):
    """Public landing page."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    context = {
        'features': [
            {'icon': 'bi-box-seam', 'title': 'Product Management',
             'desc': 'Track products with SKUs, barcodes, categories, and brands.'},
            {'icon': 'bi-graph-up-arrow', 'title': 'Real-time Analytics',
             'desc': 'Live dashboards with sales, purchases, and stock insights.'},
            {'icon': 'bi-truck', 'title': 'Supplier Management',
             'desc': 'Manage suppliers, track purchases, and automate stock updates.'},
            {'icon': 'bi-receipt', 'title': 'Sales & Invoicing',
             'desc': 'Generate invoices, apply discounts, and record transactions.'},
            {'icon': 'bi-bell', 'title': 'Smart Alerts',
             'desc': 'Get notified about low stock, out-of-stock, and new activity.'},
            {'icon': 'bi-file-earmark-bar-graph', 'title': 'Comprehensive Reports',
             'desc': 'Export CSV, print-friendly PDFs, and actionable business reports.'},
        ],
    }
    return render(request, 'core/home.html', context)


def handler_404(request, exception):
    """Custom 404 error page."""
    return render(request, 'core/404.html', status=404)


def handler_500(request):
    """Custom 500 error page."""
    return render(request, 'core/500.html', status=500)