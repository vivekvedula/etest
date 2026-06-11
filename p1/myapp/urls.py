from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_root'),                     # default home page
    path('geeks_view/', views.geeks_view, name='geeks_view'),  # shows current time
    path('test/', views.test, name='test'),                     # test page
    path('home/', views.home, name='home'),                     # home template
    path('about/', views.about, name='about'),                  # about template
    path('f/', views.r, name='r'),   
    path('form/', views.hello, name='hello'),
    path('print/',views.print,name='print'),
    path('login/', views.check_get, name='login'),
]
