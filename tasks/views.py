from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True, state=True)
    return render(request, 'tasks.html', {'tasks': tasks})
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False, state=True).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
        'forms' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form' : TaskForm,
                'error': "Ingrese datos validos"
            })
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form= TaskForm(instance=task)
        return render(request, 'tasks_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detail.html',{
                'task': task,
                'form': TaskForm,
                'error' : "Erro al actulizar la tarea ❌"
            })
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.state = False
        task.save()
        return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')