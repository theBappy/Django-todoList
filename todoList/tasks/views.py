from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout

def task_list(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  
            task.user = request.user  
            task.save()  
            return redirect('/') 
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user).order_by('-priority', 'due_date') if request.user.is_authenticated else Task.objects.none()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('/')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('/')

def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_update.html', {'form': form, 'task': task})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.set_password(form.cleaned_data['password'])
            user.save()  
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Ensure request is passed

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid username or password")  # Show error

    else:
        form = UserLoginForm()

    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  

