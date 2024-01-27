from django.shortcuts import render, redirect
from . import views
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import User

#! Usually I do this but not doing it for this project to keep the naming convention
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout





def index(request):
    return render(request,'tasks/tasks_index.html')


def user_login(request):
    
    if request.method == 'GET':
        return render(request,'tasks/user_login.html')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request,email=email,password=password)
        print(f"User: {user}")
        if user is not None:
            print(f"Logging in {user}")
            login(request,user)
            return redirect('index')
        else:
            print(f"User not found")
            error = {
                'error': 'Invalid Credentials'
            }
            return redirect('login')
    
    return render(request,'tasks/user_login.html')

def user_signup(request):
    
    if request.method == 'GET':
        return render(request,'tasks/user_signup.html')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')

        print(email,full_name,password)
        user = User.objects.create_user(email=email,full_name=full_name,password=password)
        user.save()
        
        print("User created")
        
        return redirect('login')
    
    return render(request,'tasks/user_signup.html')

def user_logout(request):
    return render(request,'tasks/user_logout.html')