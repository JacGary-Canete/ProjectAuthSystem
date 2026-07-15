from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('laptops/', views.laptop_list, name='laptop_list'),
    path('laptops/add/', views.laptop_add, name='laptop_add'),
    path('browse-laptops/', views.browse_laptops, name='browse_laptops'),
    path('borrow/<int:laptop_id>/', views.borrow_laptop, name='borrow_laptop'),
    path('return/<int:loan_id>/', views.return_laptop, name='return_laptop'),
    path('laptops/<int:laptop_id>/edit/', views.laptop_edit, name='laptop_edit'),
    path('approve-return/<int:loan_id>/', views.approve_return, name='approve_return'),
    path('loan-history/', views.loan_history, name='loan_history'),
    path('approve-loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('reject-return/<int:loan_id>/', views.reject_return, name='reject_return'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='myapp/password_reset.html',
        email_template_name='myapp/password_reset_email.html',
        subject_template_name='myapp/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='myapp/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myapp/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='myapp/password_reset_complete.html'
    ), name='password_reset_complete'),

]