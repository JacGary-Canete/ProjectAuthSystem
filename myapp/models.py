from django.db import models
from django.contrib.auth.models import User

class Laptop(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('maintenance', 'Under Maintenance'),
    ]

    asset_tag = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    processor = models.CharField(max_length=100, blank=True)
    ram_gb = models.PositiveIntegerField(null=True, blank=True)
    storage_gb = models.PositiveIntegerField(null=True, blank=True)
    battery_health = models.PositiveIntegerField(null=True, blank=True, help_text="Battery health percentage")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateField(null=True, blank=True)
    condition_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.brand} {self.model}"