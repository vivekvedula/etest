from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import TestForm, QuestionForm
from .models import Test, Question, Result

User = get_user_model()


# -------------------------
# HOME
# -------------------------
def home(request):
    return render(request, 'myapp/home.html')


# -------------------------
# ADMIN LOGIN
# -------------------------
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dash')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'myapp/admin_login.html')


# -------------------------
# STUDENT LOGIN
# -------------------------
def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user and not user.is_superuser:
            login(request, user)
            return redirect('student_dash')
        else:
            messages.error(request, "Invalid student credentials")

    return render(request, 'myapp/student_login.html')


# -------------------------
# ADMIN DASHBOARD
# -------------------------
def admin_dash(request):
    return render(request, 'myapp/admin_dash.html', {
        'total_tests': Test.objects.count(),
        'total_students': User.objects.filter(is_superuser=False).count(),
        'total_admins': User.objects.filter(is_superuser=True).count(),
        'total_results': Result.objects.count()
    })


# -------------------------
# CREATE ACCOUNT
# -------------------------
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect('create_account')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()
        return redirect('home')

    return render(request, 'myapp/create_account.html')


# -------------------------
# TEST MANAGEMENT
# -------------------------
def create_test(request):
    form = TestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_dash')
    return render(request, 'myapp/create_test.html', {'form': form})


def add_question(request):
    form = QuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_dash')
    return render(request, 'myapp/add_question.html', {'form': form})


def view_tests(request):
    tests = Test.objects.all().order_by('-created_at')
    return render(request, 'myapp/view_tests.html', {'tests': tests})


def view_questions(request):
    questions = Question.objects.all().order_by('-id')
    return render(request, 'myapp/view_questions.html', {'questions': questions})


# -------------------------
# START TEST
# -------------------------
def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test)

    return render(request, 'myapp/start_test.html', {
        'test': test,
        'questions': questions
    })


# -------------------------
# SUBMIT TEST
# -------------------------
@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test)

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_option:
                score += 1

        Result.objects.create(
            user=request.user,
            test=test,
            score=score
        )

        return render(request, 'myapp/result.html', {
            'score': score,
            'test': test
        })

    return redirect('student_dash')


# -------------------------
# VIEW RESULTS (ADMIN)
# -------------------------
def view_results(request):
    results = Result.objects.all().order_by('-submitted_at')
    return render(request, 'myapp/view_results.html', {'results': results})


# -------------------------
# STUDENT DASHBOARD (FINAL FIXED)
# -------------------------
@login_required
def stud_dash(request):
    user = request.user

    available_tests = Test.objects.all()
    completed_tests = Result.objects.filter(user=user)

    total_attempts = completed_tests.count()
    total_score = sum(r.score for r in completed_tests)
    total_max = sum(r.test.total_marks for r in completed_tests)

    percentage = round((total_score / total_max) * 100, 2) if total_max > 0 else 0

    return render(request, 'myapp/stud_dash.html', {
        'available_tests': available_tests,
        'completed_tests': completed_tests,
        'total_attempts': total_attempts,
        'total_score': total_score,
        'total_max': total_max,
        'percentage': percentage
    })