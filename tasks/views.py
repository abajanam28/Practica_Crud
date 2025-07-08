from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        # print('enviando formulario')
        return render(request, 'signup.html', {
            'forms' : UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Register user and save
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(tasks)
            except IntegrityError:
                return render(request, 'signup.html', {
                    'forms' : UserCreationForm,
                    'error' : "El usuario ya existe"
                })
        return render(request, 'signup.html', {
                    'forms' : UserCreationForm,
                    'error' : "La contraseña es incorrecta"
                })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'forms': AuthenticationForm,
        })
    else:
        user = authenticate(request, username= request.POST['username'],
                password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'forms': AuthenticationForm,
                'error' : "El usuario o contraseña es incorrecto!!"
            })
        else:
            login(request, user)
            return redirect('tasks')



def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')