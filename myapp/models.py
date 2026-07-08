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

class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='loans')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrower')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='loans_processed')
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateTimeField(null=True, blank=True)
    loan_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.laptop.asset_tag} - {self.borrower.username} {self.loan_status}"