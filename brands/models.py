from django.db import models


class Brand(models.Model):
    """Product brand model."""
    name = models.CharField(max_length=150, unique=True, db_index=True)
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
        indexes = [models.Index(fields=['name', 'status'])]

    def __str__(self):
        return self.name