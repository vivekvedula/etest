from django.shortcuts import render
from django.http import HttpResponse
# import datetime
import datetime

# create a function-based view
def geeks_view(request):
    # fetch current date and time
    now = datetime.datetime.now()
    # convert to string
    html = "Time is {}".format(now)
    # return HttpResponse
    return HttpResponse(html)
def test(request):
    return HttpResponse("Hello! This is the test page.")
def about(request):
    return render(request, 'myapp/about.html')
def r(request):
    return HttpResponse('no defined tempelate')
def hello(request):
    number = request.GET.get('num')  # returns string or None

    return render(request, 'myapp/form.html', {'number': number})
def print(request):
    s=int(input('ee'))
    return HttpResponse(f'print no {s}')
def home(request):
    # Hardcoded context data
    context = {
        "name": "Alice",
        "age": 25,
        "hobbies": ["Reading", "Coding", "Traveling"]
    }
    return render(request, "myapp/home.html", context)
def check_details(request):
    message = ""  # Default message

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username == "a" and email == "a@gmail.com" and password == "123456":
            message = "Login Successful"
        else:
            message = "Wrong Details"

    return render(request, "myapp/details.html", {"message": message})
def check_get(request):
    message = ""

    if 'username' in request.GET and 'password' in request.GET:
        username = request.GET.get("username")
        password = request.GET.get("password")

        if username and password:
            message = f"Welcome, {username}!"
        else:
            message = "Please enter both username and password"

    return render(request, "myapp/get.html", {"message": message})