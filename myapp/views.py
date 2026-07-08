from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .models import Laptop, Loan
from .forms import LaptopForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_staff = (form.cleaned_data['role'] == 'staff')
            user.save()
            messages.success(request, 'Account created successfully! You may now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('dashboard_home')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'myapp/login.html')

@login_required
def student_dashboard(request):
    available_count = Laptop.objects.filter(status='available').count()
    active_loans = Loan.objects.filter(borrower=request.user, loan_status='active')
    return render(request, 'myapp/student_dashboard.html', {
        'available_count': available_count,
        'active_loans': active_loans,
    })
def logout_view(request):
    logout(request)
    return redirect('login')

def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user, login_url='login')
def dashboard_home(request):
    laptops = Laptop.objects.all()
    return render(request, 'myapp/home.html', {'laptops': laptops})

@login_required
@user_passes_test(is_staff_user, login_url='login')
def laptop_list(request):
    laptops = Laptop.objects.all()
    return render(request, 'myapp/laptop_list.html', {'laptops': laptops})

@login_required
@user_passes_test(is_staff_user, login_url='login')
def laptop_add(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laptop added to inventory.')
            return redirect('laptop_list')
    else:
        form = LaptopForm()
    return render(request, 'myapp/laptop_add.html', {'form': form})
