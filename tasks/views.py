from django.shortcuts import render, redirect, HttpResponse
from . import views
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import User, Task, TaskPhoto

#! Usually I do this but not doing it for this project to keep the naming convention
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout


def index(request):
    if request.user.is_authenticated:
        # Get tasks for the logged-in user
        user_tasks = Task.objects.filter(user=request.user)
        user_tasks = Task.objects.filter(
            user=request.user).prefetch_related('photos')
        return render(request, 'tasks/tasks_index.html', {'tasks': user_tasks})
    else:
        return redirect('login')
    

def user_login(request):

    if request.method == 'GET':
        return render(request, 'tasks/user_login.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(f"User: {user}")
        if user is not None:
            print(f"Logging in {user}")
            login(request, user)
            return redirect('index')
        else:
            print(f"User not found")
            error = {
                'error': 'Invalid Credentials'
            }
            return redirect('login')

    return render(request, 'tasks/user_login.html')


def user_signup(request):

    if request.method == 'GET':
        return render(request, 'tasks/user_signup.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')

        print(email, full_name, password)
        user = User.objects.create_user(
            email=email, full_name=full_name, password=password)
        user.save()

        print("User created")

        return redirect('login')

    return render(request, 'tasks/user_signup.html')


def user_logout(request):
    return render(request, 'tasks/user_logout.html')


def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        print(request.POST)
        print(request.FILES)
        
        task = Task(title=title, description=description, due_date=due_date, user=request.user)
        task.save()
        
        for file in request.FILES.getlist('photos'):
            try:
                TaskPhoto.objects.create(task=task, photo=file)
            except Exception as e:
                print(f"TaskImage Failed! Exception: {e}")
        
        return redirect('index')
    return render(request, 'tasks/create_task.html')


def delete_task_photo(request, photo_id):
    # Ensure the user is authorized to delete the photo
    photo = TaskPhoto.objects.get(id=photo_id)
    if photo.task.user == request.user:  # Check ownership
        photo.delete()
        return HttpResponse('Photo deleted')
    else:
        return HttpResponse('Unauthorized', status=401)


def edit(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect('index')
    return render(request, 'tasks/edit.html', {'task': task})