from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
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
