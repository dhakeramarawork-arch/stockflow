from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_overview, name='overview'),
    path('movements/', views.stock_movements, name='movements'),
    path('adjustment/', views.stock_adjustment, name='adjustment'),
]