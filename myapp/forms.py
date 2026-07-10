import re
from django import forms
from django.contrib.auth.models import User
from myapp.models import Laptop


class RegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('staff', 'Staff / IT Admin'),
        ('student', 'Student'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password:
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("Password must contain at least one number.")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")

        return cleaned_data

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['asset_tag', 'brand', 'model', 'processor', 'ram_gb', 'storage_gb', 'battery_health', 'status',
                  'purchase_date', 'condition_notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }