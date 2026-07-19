from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index, name='index'),
    path('sales/', views.sales_report, name='sales'),
    path('purchases/', views.purchase_report, name='purchases'),
    path('inventory/', views.inventory_report, name='inventory'),
    path('profit/', views.profit_report, name='profit'),
    path('low-stock/', views.low_stock_report, name='low_stock'),
    path('suppliers/', views.supplier_report, name='suppliers'),
    path('customers/', views.customer_report, name='customers'),
]