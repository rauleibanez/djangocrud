from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TaskForm 
from .models import Task
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks':tasks, 'titlePage': 'Tasks Pending'})

@login_required
def tasks_done(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks':tasks, 'titlePage': 'Tasks Completed'})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form':TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_Task = form.save(commit=False)
            new_Task.user = request.user
            new_Task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form':TaskForm, 'error':'Por favor coloque datos validos'})

@login_required        
def task_details(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_details.html', {'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_details.html', {'task':task, 'form':form, 'error':'Error Actualizando Datos'})

@login_required
def task_completed(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks') 

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks') 

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            #registro el usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # inicio de sesion autimatico del usuario
                login(request, user)
                return redirect('tasks')
                # return HttpResponse('Usuario creado Satisfactoriamente!')
            except:
                # return HttpResponse('Error Usuario Existente!')
                return render(request, 'signup.html', {'form':UserCreationForm, 'error':'Error Usuario Existente!'})
        else:
            # mensaje de error
            # return HttpResponse('Las constraseñas no coinciden!')
            return render(request, 'signup.html', {'form':UserCreationForm, 'error':'Las constraseñas no coinciden!'})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form':AuthenticationForm})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form':AuthenticationForm, 'error':'Usuario o Password Incorrectos!'})
        else:
            login(request, user)
            return redirect('tasks')