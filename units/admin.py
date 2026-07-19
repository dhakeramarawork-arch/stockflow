from django.contrib import admin
from .models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'short_code')