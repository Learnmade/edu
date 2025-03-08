from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here
def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  # Change to the page you want after login
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")

def register_user(request):

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists")
            return redirect('/register/')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username )
        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully")
        return redirect('/register/')
    return render(request, 'register.html')
