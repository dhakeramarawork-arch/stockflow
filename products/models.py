from django.db import models
from categories.models import Category
from brands.models import Brand
from units.models import Unit
from suppliers.models import Supplier


class Product(models.Model):
    """Main product model with full inventory fields."""
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    barcode = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True,
                              related_name='products')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True,
                             related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,
                                 related_name='products')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                              help_text='Tax percentage')
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'status']),
            models.Index(fields=['sku', 'barcode']),
        ]

    def __str__(self):
        return f'{self.name} ({self.sku})'

    @property
    def stock_status(self):
        """Return stock status badge label."""
        if self.current_stock == 0:
            return 'out_of_stock'
        elif self.current_stock <= self.minimum_stock:
            return 'low_stock'
        return 'in_stock'

    @property
    def stock_value(self):
        """Current inventory value based on purchase price."""
        return self.current_stock * self.purchase_price

    @property
    def profit_margin(self):
        """Profit margin percentage."""
        if self.selling_price > 0:
            return ((self.selling_price - self.purchase_price) / self.selling_price) * 100
        return 0