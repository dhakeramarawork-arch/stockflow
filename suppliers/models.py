from django.db import models


class Supplier(models.Model):
    """Supplier model."""
    company_name = models.CharField(max_length=255, db_index=True)
    contact_person = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=30, db_index=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    gst_vat = models.CharField(max_length=50, blank=True, null=True, verbose_name='GST/VAT')
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']
        indexes = [models.Index(fields=['company_name', 'status'])]

    def __str__(self):
        return self.company_name