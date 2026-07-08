from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import RegisterForm, LaptopForm
from .models import Laptop, Loan


def is_staff_user(user):
    return user.is_staff


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


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(is_staff_user, login_url='login')
def dashboard_home(request):
    laptops = Laptop.objects.all()
    active_loans = Loan.objects.filter(loan_status='active')
    return render(request, 'myapp/home.html', {'laptops': laptops, 'active_loans': active_loans})


@login_required
def student_dashboard(request):
    available_count = Laptop.objects.filter(status='available').count()
    active_loans = Loan.objects.filter(borrower=request.user, loan_status='active')
    return render(request, 'myapp/student_dashboard.html', {
        'available_count': available_count,
        'active_loans': active_loans,
    })


@login_required
def browse_laptops(request):
    laptops = Laptop.objects.filter(status='available')
    return render(request, 'myapp/browse_laptops.html', {'laptops': laptops})


@login_required
def borrow_laptop(request, laptop_id):
    laptop = Laptop.objects.get(id=laptop_id)

    if laptop.status != 'available':
        messages.error(request, 'This laptop is no longer available.')
        return redirect('browse_laptops')

    Loan.objects.create(
        laptop=laptop,
        borrower=request.user,
        due_date=timezone.now() + timedelta(days=7),
        loan_status='active',
    )
    laptop.status = 'borrowed'
    laptop.save()

    messages.success(request, f'You have borrowed {laptop.brand} {laptop.model}. Due in 7 days.')
    return redirect('student_dashboard')


@login_required
def return_laptop(request, loan_id):
    loan = Loan.objects.get(id=loan_id, borrower=request.user)

    if loan.loan_status != 'active':
        messages.error(request, 'This loan is not active.')
        return redirect('student_dashboard')

    loan.return_date = timezone.now()
    loan.loan_status = 'returned'
    loan.save()

    loan.laptop.status = 'available'
    loan.laptop.save()

    messages.success(request, f'You have returned {loan.laptop.brand} {loan.laptop.model}.')
    return redirect('student_dashboard')


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


@login_required
@user_passes_test(is_staff_user, login_url='login')
def laptop_edit(request, laptop_id):
    laptop = Laptop.objects.get(id=laptop_id)
    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laptop updated.')
            return redirect('laptop_list')
    else:
        form = LaptopForm(instance=laptop)
    return render(request, 'myapp/laptop_edit.html', {'form': form, 'laptop': laptop})


@login_required
@user_passes_test(is_staff_user, login_url='login')
def process_checkin(request, loan_id):
    loan = Loan.objects.get(id=loan_id)

    if loan.loan_status != 'active':
        messages.error(request, 'This loan is not active.')
        return redirect('dashboard_home')

    loan.return_date = timezone.now()
    loan.loan_status = 'returned'
    loan.processed_by = request.user
    loan.save()

    loan.laptop.status = 'available'
    loan.laptop.save()

    messages.success(request, f'Checked in {loan.laptop.asset_tag} from {loan.borrower.username}.')
    return redirect('dashboard_home')