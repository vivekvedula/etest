from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('admin_dash/', views.admin_dash, name='admin_dash'),
    path('student_dash/', views.student_dash, name='student_dash'),
    path('create_account/', views.create_account, name='create_account'),

]