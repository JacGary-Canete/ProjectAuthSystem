from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('return_pending', 'Return Pending Approval'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='loans')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans_borrowed')
    checkout_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='checkouts_approved')
    return_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='returns_approved')
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    loan_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='returns_rejected')
    rejected_at = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        if self.loan_status == 'active' and self.due_date:
            return timezone.now() > self.due_date
        return False

    def __str__(self):
        return f"{self.laptop.asset_tag} → {self.borrower.username} ({self.loan_status})"

class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='login_attempt')
    failed_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    def is_locked(self):
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False