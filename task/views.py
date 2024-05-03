from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .form import TaskForm
from .models import Task
# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'register/register.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('home')
            except:
                return render(request, 'register/register.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'register/register.html', {
                'form': UserCreationForm,
                'error': 'completar todos los campos'
            })


def signin(request):
    if request.method == 'GET':
        return render(request, 'login/login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login/login.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password are incorrects'
            })


def signout(request):
    logout(request)
    return redirect('home')


def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task/create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('home')
        except ValueError:
            return render(request, 'tasks/create_task/create_task.html', {
                'form': TaskForm,
                'error': 'Complete todos los campos'
            })


def all_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'tasks/all_tasks/all_tasks.html', {
            'tasks': tasks
        })


def pending_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(
            user=request.user, datecompleted__isnull=True)
        return render(request, 'tasks/pending_tasks/pending_tasks.html', {'tasks': tasks})


def completed_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(
            user=request.user, datecompleted__isnull=False)
        return render(request, 'tasks/completed_tasks/completed_tasks.html', {'tasks': tasks})


def detail_task(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'tasks/detail_task/detail_task.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('alltasks')
        except ValueError:
            return render(request, 'tasks/detail_tasks/detail_tasks.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })


def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('home')


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
