from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'phone', 'city', 'status')
    list_filter = ('status', 'city', 'country')
    search_fields = ('company_name', 'contact_person', 'phone', 'email')