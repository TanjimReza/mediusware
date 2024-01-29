from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import views
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import TaskUser, Task, TaskPhoto
from django.contrib import messages
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
#! Usually I do this but not doing it for this project to keep the naming convention
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_index.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        search_query = self.request.GET.get('search', '')
        creation_date = self.request.GET.get('creation_date', 'Last')
        completion_status = self.request.GET.get('completion_status', 'all')
        priority = self.request.GET.get('priority', 'all')

        print(self.request.GET)
        print(search_query, creation_date, completion_status, priority)

        # if completion_status != 'all':
        #     queryset = queryset.filter(status=completion_status)

        if search_query == '':
            print("No search query")

        else:
            queryset = queryset.filter(title__icontains=search_query)

        if creation_date == 'Last':
            queryset = queryset.order_by('-created_at')
        elif creation_date == 'First':
            queryset = queryset.order_by('created_at')

        if completion_status == 'pending':
            queryset = queryset.filter(status='pending')
        elif completion_status == 'completed':
            queryset = queryset.filter(status='completed')

        if priority == 'low':
            queryset = queryset.filter(priority='low')
        elif priority == 'medium':
            queryset = queryset.filter(priority='medium')
        elif priority == 'high':
            queryset = queryset.filter(priority='high')

        return queryset


class UserLoginView(View):
    template_name = 'tasks/user_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(f"TaskUser: {user}")
        if user is not None:
            print(f"Logging in {user}")
            login(request, user)
            return redirect('task_list')
        else:
            print(f"TaskUser not found")
            error = {
                'error': 'Invalid Credentials'
            }
            return render(request, self.template_name, error)


class UserSignupView(View):
    template_name = 'tasks/user_signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')

        user = TaskUser.objects.create_user(
            email=email, full_name=full_name, password=password)
        user.save()

        return redirect('login')


def user_logout(request):
    logout(request)

    return render(request, 'tasks/user_logout.html')


class TaskCreateView(LoginRequiredMixin, View):
    template_name = 'tasks/create_task.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        priority = request.POST.get('priority')

        task = Task(title=title, description=description,
                    due_date=due_date, user=request.user, status=status, priority=priority)
        task.save()

        for file in request.FILES.getlist('photos'):
            try:
                TaskPhoto.objects.create(task=task, photo=file)
            except Exception as e:
                print(f"TaskImage Failed! Exception: {e}")

        return redirect('task_list')


class DeleteTaskPhotoView(LoginRequiredMixin, View):

    def get(self, request, photo_id):
        photo = TaskPhoto.objects.get(id=photo_id)
        if photo.task.user == request.user:
            photo.delete()
            return HttpResponse('Photo deleted')
        else:
            return HttpResponse('Unauthorized', status=401)


class DeleteTaskView(LoginRequiredMixin, View):
    template_name = 'tasks/confirm_delete.html'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        return render(request, self.template_name, {'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')


@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date')

        task.save()

        for file in request.FILES.getlist('photos'):
            try:
                TaskPhoto.objects.create(task=task, photo=file)
            except Exception as e:
                print(f"Error uploading photo: {e}")

        return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {'task': task})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    photos = task.photos.all()
    return render(request, 'tasks/task_detail.html', {'task': task, 'photos': photos})
