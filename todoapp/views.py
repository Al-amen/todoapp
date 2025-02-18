from django.shortcuts import render,redirect
from todoapp.forms import UserRegistrationForm,CreateTasksForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from todoapp.models import Task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.cache import cache
import secrets
from django.http import HttpResponseBadRequest



@login_required
def hello_protected(request):
    return render(request, 'todoapp/protected.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user=user)
            return redirect('task_list')
            
           
    else:
        form = UserRegistrationForm()
    return render(request, 'todoapp/register.html', {'form': form})


def authenticate_via_magic_link(request, token):
    email = None
    for key in cache._cache.keys():
        if cache.get(key) == token:
            email = key
            break
    if email is None:
        return HttpResponseBadRequest(content="Magic Link invalid/expired")
    
    user = User.objects.filter(email=email).first()
    if user:
        user.is_active = True
        user.save()
        login(request, user)
        cache.delete(email)
        return redirect('task_list')
    else:
        return HttpResponseBadRequest(content="User not found")

@login_required
def user_logout(request):
     logout(request)
     return redirect('login')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todoapp/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = CreateTasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
            
    else:
        form = CreateTasksForm()

        return render(request, 'todoapp/create_task.html', {'form': form})
    
@login_required
def task_edit(request,pk):
   task = Task.objects.get(pk=pk, user=request.user)
   if request.method == 'POST':
            form = CreateTasksForm(request.POST,instance=task)
            if form.is_valid():
                form.save()
                return redirect('task_list')
   else:
      form = CreateTasksForm(instance=task)
      return render(request, 'todoapp/create_task.html', {'form': form})   

        
@login_required
def task_delete(request,pk):
    task = Task.objects.get(pk=pk, user=request.user)

    task.delete()
    return redirect('task_list')