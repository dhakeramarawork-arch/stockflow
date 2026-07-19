from django.db import models


class Unit(models.Model):
    """Measurement unit (Piece, Box, Kg, Litre, etc.)."""
    name = models.CharField(max_length=50, unique=True, db_index=True)
    short_code = models.CharField(max_length=20, unique=True, help_text='e.g. pc, kg, ltr')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.short_code})'