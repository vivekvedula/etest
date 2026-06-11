from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test


User = get_user_model()  # This returns your custom myapp.User
def admin_login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_superuser:
            login(request, user) 
            return redirect('admin_dash') 
        else:
            messages.error(request, "Invalid credentials or not an admin")
    
    return render(request, 'myapp/admin_login.html')
def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find user by email
            user_obj = User.objects.get(email=email)
            # Authenticate using username + password
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and getattr(user, 'is_student', False):
            # Log in student
            login(request, user)
            return redirect('student_dash')  # redirect to student dashboard
        else:
            messages.error(request, "Invalid credentials or not a student")
    return render(request, 'myapp/student_login.html')   
def admin_dash(request):
    total_tests = 1  # placeholder, replace with actual Test.objects.count() later
    total_students = User.objects.filter(is_student=True).count()
    total_admins = User.objects.filter(is_superuser=True).count()
    all_users = User.objects.all()
    context = {
        'total_tests': total_tests,
        'total_students': total_students,
        'total_admins': total_admins,
        'all_users': all_users
    }
    
    return render(request, 'myapp/admin_dash.html', context)
def student_dash(request):
    return render(request, 'myapp/stud_dash.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('create_account')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('create_account')

        if role == 'student':
            user = User.objects.create_user(username=username, email=email, password=password, is_student=True)
            user.save()
            messages.success(request, 'Student account created successfully! Please log in.')
            return redirect('student_login')
        elif role == 'admin':
            user = User.objects.create_user(username=username, email=email, password=password, is_admin=True, is_superuser=True, is_staff=True)
            user.save()
            messages.success(request, 'Admin account created successfully! Please log in.')
            return redirect('admin_login')

    return render(request, 'myapp/create_account.html')

