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
    pending_requests = Loan.objects.filter(loan_status='pending')
    return_requests = Loan.objects.filter(loan_status='return_pending')
    active_loans = Loan.objects.filter(loan_status='active')
    return render(request, 'myapp/home.html', {
        'laptops': laptops,
        'pending_requests': pending_requests,
        'return_requests': return_requests,
        'active_loans': active_loans,
    })


@login_required
def student_dashboard(request):
    available_count = Laptop.objects.filter(status='available').count()
    active_loans = Loan.objects.filter(borrower=request.user, loan_status='active')
    pending_loans = Loan.objects.filter(borrower=request.user, loan_status='pending')
    return render(request, 'myapp/student_dashboard.html', {
        'available_count': available_count,
        'active_loans': active_loans,
        'pending_loans': pending_loans,
    })


@login_required
def browse_laptops(request):
    laptops = Laptop.objects.filter(status='available')
    return render(request, 'myapp/browse_laptops.html', {'laptops': laptops})


@login_required
def borrow_laptop(request, laptop_id):
    if Loan.objects.filter(borrower=request.user, loan_status__in=['pending', 'active']).exists():
        messages.error(request, 'You already have a pending or active loan.')
        return redirect('browse_laptops')

    laptop = Laptop.objects.get(id=laptop_id)

    if laptop.status != 'available':
        messages.error(request, 'This laptop is no longer available.')
        return redirect('browse_laptops')

    Loan.objects.create(
        laptop=laptop,
        borrower=request.user,
        loan_status='pending',
    )

    messages.success(request, f'Request sent for {laptop.brand} {laptop.model}. Waiting for staff approval.')
    return redirect('student_dashboard')

@login_required
def return_laptop(request, loan_id):
    loan = Loan.objects.get(id=loan_id, borrower=request.user)

    if loan.loan_status != 'active':
        messages.error(request, 'This loan is not active.')
        return redirect('student_dashboard')

    loan.loan_status = 'return_pending'
    loan.save()

    messages.success(request, f'Return requested for {loan.laptop.brand} {loan.laptop.model}. Waiting for staff to inspect and approve.')
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
def loan_history(request):
    returned_loans = Loan.objects.filter(loan_status='returned').order_by('-return_date')
    rejected_returns = Loan.objects.exclude(rejection_reason='').order_by('-rejected_at')
    return render(request, 'myapp/loan_history.html', {
        'returned_loans': returned_loans,
        'rejected_returns': rejected_returns,
    })
@login_required
@user_passes_test(is_staff_user, login_url='login')
def approve_loan(request, loan_id):
    loan = Loan.objects.get(id=loan_id)

    if loan.loan_status != 'pending':
        messages.error(request, 'This request is no longer pending.')
        return redirect('dashboard_home')

    loan.loan_status = 'active'
    loan.due_date = timezone.now() + timedelta(days=7)
    loan.checkout_approved_by = request.user
    loan.save()

    loan.laptop.status = 'borrowed'
    loan.laptop.save()

    messages.success(request, f'Approved: {loan.laptop.asset_tag} checked out to {loan.borrower.username}.')
    return redirect('dashboard_home')

@login_required
@user_passes_test(is_staff_user, login_url='login')
def approve_return(request, loan_id):
    loan = Loan.objects.get(id=loan_id)

    if loan.loan_status != 'return_pending':
        messages.error(request, 'This loan has no pending return request.')
        return redirect('dashboard_home')

    loan.return_date = timezone.now()
    loan.loan_status = 'returned'
    loan.return_approved_by = request.user
    loan.save()

    loan.laptop.status = 'available'
    loan.laptop.save()

    messages.success(request, f'Return approved for {loan.laptop.asset_tag} from {loan.borrower.username}.')
    return redirect('dashboard_home')

@login_required
@user_passes_test(is_staff_user, login_url='login')
def reject_return(request, loan_id):
    loan = Loan.objects.get(id=loan_id)

    if loan.loan_status != 'return_pending':
        messages.error(request, 'This loan has no pending return request.')
        return redirect('dashboard_home')

    reason = request.POST.get('reason', '').strip()
    if not reason:
        messages.error(request, 'A reason is required to reject a return.')
        return redirect('dashboard_home')

    loan.loan_status = 'active'
    loan.rejection_reason = reason
    loan.rejected_by = request.user
    loan.rejected_at = timezone.now()
    loan.save()

    messages.success(request, f'Return rejected for {loan.laptop.asset_tag}. Laptop remains checked out.')
    return redirect('dashboard_home')

