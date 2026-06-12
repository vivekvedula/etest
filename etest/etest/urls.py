from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('admin_login/', views.admin_login, name='admin_login'),
    path('student_login/', views.student_login, name='student_login'),

    path('admin_dash/', views.admin_dash, name='admin_dash'),

    path('stud_dash/', views.stud_dash, name='student_dash'),

    path('create_account/', views.create_account, name='create_account'),

    path('create_test/', views.create_test, name='create_test'),
    path('view_tests/', views.view_tests, name='view_tests'),

    path('add_question/', views.add_question, name='add_question'),
    path('view_questions/', views.view_questions, name='view_questions'),

    path('start_test/<int:test_id>/', views.start_test, name='start_test'),
    path('submit_test/<int:test_id>/', views.submit_test, name='submit_test'),

    path('view_results/', views.view_results, name='view_results'),
]