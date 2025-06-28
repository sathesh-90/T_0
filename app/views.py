from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db import models

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Replace with your login view name

    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')  # Get the "Remember Me" checkbox value

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if not remember:
                # Set session to expire when the browser is closed
                request.session.set_expiry(0)
            else:
                # Set session to persist for the default duration
                request.session.set_expiry(None)

            messages.success(request, '✅ Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, '❌ Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status') or 'incomplete'
        priority = request.POST.get('priority') or 'medium'

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            priority=priority,
        )

        messages.success(request, '✅ Task added successfully.')
        return redirect('task_list')
    
    status = request.GET.get('status')  # Get the 'status' query parameter
    if status:
        tasks = Task.objects.filter(status=status)  # Filter tasks by status
    else:
        tasks = Task.objects.all()  # Show all tasks if no status is specified

    return render(request, 'add_task.html')






from django.contrib.auth.decorators import login_required




def task_list(request):
    status = request.GET.get('status')  # Get the 'status' query parameter
    query = request.GET.get('q')  # Get the 'q' query parameter for search

    # Start with base queryset filtered by logged-in user
    tasks = Task.objects.filter(user=request.user)

    # Apply additional filters if they exist
    if status:
        tasks = tasks.filter(status=status)  # Maintain user filter and add status filter

    if query:
        tasks = tasks.filter(title__icontains=query)  # Maintain all previous filters and add search

    return render(request, 'task_list.html', {'tasks': tasks})






@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id,user=request.user)# Ensure the task belongs to the logged-in user
    status = request.GET.get('status')  # Get the 'status' query parameter
    if status:
        tasks = Task.objects.filter(status=status)  # Filter tasks by status
    else:
        tasks = Task.objects.all()  # Show all tasks if no status is specified

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.save()
        messages.success(request, '✅ Task updated successfully.')
        return redirect('task_list')

    return render(request, 'edit_task.html', {'task': task})


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id,user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('task_list')

# filepath: /home/rguktrkvalley/Documents/Tasker/app/views.py

import csv



@login_required
def export_excel(request):
    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Due Date', 'Status', 'Priority'])

    # Fetch tasks and write to CSV
    tasks = Task.objects.all()
    for task in tasks:
        writer.writerow([task.title, task.description, task.due_date, task.status, task.priority])

    return response
from django.shortcuts import render
from .models import Task




@login_required
def dashboard(request):
    # Filter all tasks by the current user
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    incomplete = tasks.filter(status='incomplete').count()
    progressing = tasks.filter(status='progressing').count()
    completed = tasks.filter(status='completed').count()

    # Generate data for the line chart (tasks by due date)
    due_data = {
        'labels': [],
        'counts': [],
    }

    # Group tasks by due date and count them
    due_date_counts = tasks.values('due_date').annotate(count=models.Count('id')).order_by('due_date')
    for entry in due_date_counts:
        due_data['labels'].append(entry['due_date'].strftime('%Y-%m-%d'))  # Format date as string
        due_data['counts'].append(entry['count'])

    # Data for the bar chart (tasks by status)
    chart_data = {
        'labels': ['Incomplete', 'Progressing', 'Completed'],
        'counts': [incomplete, progressing, completed],
    }

    return render(request, 'dashboard.html', {
        'total': total,
        'incomplete': incomplete,
        'progressing': progressing,
        'completed': completed,
        'chart_data': chart_data,
        'due_data': due_data,
    })
    from django.contrib.auth.decorators import login_required



def settings(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = request.user
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()

        messages.success(request, '✅ Settings updated successfully.')
        return redirect('login')  # Redirect to the settings page after saving

    return render(request, 'settings.html')