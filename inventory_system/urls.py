"""Main URL configuration for the Inventory Management System."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Home / landing page
    path('', include('core.urls')),
    # Authentication
    path('accounts/', include('accounts.urls')),
    # Dashboard
    path('dashboard/', include('dashboard.urls')),
    # Modules
    path('categories/', include('categories.urls')),
    path('brands/', include('brands.urls')),
    path('units/', include('units.urls')),
    path('products/', include('products.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('customers/', include('customers.urls')),
    path('purchases/', include('purchases.urls')),
    path('sales/', include('sales.urls')),
    path('inventory/', include('inventory.urls')),
    path('reports/', include('reports.urls')),
    # Django admin (management only)
    path('admin/', admin.site.urls),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'core.views.handler_404'
handler500 = 'core.views.handler_500'