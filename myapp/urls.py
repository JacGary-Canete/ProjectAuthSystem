from django.urls import path
from . import views

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
    path('process-checkin/<int:loan_id>/', views.process_checkin, name='process_checkin'),

]