from django.db import models
from products.models import Product


class StockMovement(models.Model):
    """Tracks every stock movement (in/out/adjustment)."""
    MOVEMENT_TYPES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('adjustment', 'Adjustment'),
        ('damaged', 'Damaged'),
        ('expired', 'Expired'),
        ('transfer', 'Transfer'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                   help_text='Positive for in, negative for out')
    reference = models.CharField(max_length=100, blank=True, null=True,
                                 help_text='Invoice or purchase number')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['product', 'movement_type'])]

    def __str__(self):
        return f'{self.product.name} - {self.movement_type} - {self.quantity}'