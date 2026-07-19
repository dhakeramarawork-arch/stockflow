from django.contrib import admin
from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchase_number', 'supplier', 'purchase_date', 'total', 'payment_status')
    list_filter = ('payment_status', 'purchase_date')
    search_fields = ('purchase_number', 'supplier__company_name')
    inlines = [PurchaseItemInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product', 'quantity', 'unit_cost', 'total')