from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import TaskForm, SignUpForm, CategoryForm
from .models import Task, Category
from django.db.models import Q

@login_required
def task_list(request):
    query = request.GET.get('query', '')
    priority_str = request.GET.get('priority', '')
    status_str = request.GET.get('status', '') #status filtering
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Priority mapping from string to integer
    priority_mapping = {
        'high': 1,
        'medium': 2,
        'low': 3,
    }
    
    # Initialize the task queryset for the logged-in user
    tasks = Task.objects.filter(user=request.user)

    # Filter by query string
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    # Convert string priority to integer
    priority = priority_mapping.get(priority_str.lower()) if priority_str else None
    
    # Filter by priority if provided
    if priority is not None:
        tasks = tasks.filter(priority=priority)
    
    # Filter by status if provided
    if status_str:
        tasks = tasks.filter(status=status_str)

    # Filter by date range
    if start_date and end_date:
        tasks = tasks.filter(due_date__range=[start_date, end_date])
    elif start_date:
        tasks = tasks.filter(due_date__gte=start_date)
    elif end_date:
        tasks = tasks.filter(due_date__lte=end_date)

    # Render the task list template with the context
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'query': query,
        'priority': priority_str,  # Keep it as string for the template
        'status': status_str,  # Keep the status filter as a string for the template
        'start_date': start_date,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request=request)  # Pass request to the form
        if form.is_valid():
            task = form.save(commit=False)  # Save will handle setting the user
            task.user = request.user  # Set the user to the logged-in user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(request=request)  # Pass request to the form
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user != request.user:
        messages.error(request, "You do not have permission to edit this task.")
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, request=request)  # Pass request to the form
        if form.is_valid():
            form.save()  # Save will handle updating the task
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, request=request)  # Pass request to the form
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user != request.user:
        messages.error(request, "You do not have permission to delete this task.")
        return redirect('task_list')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Account created and logged in as {username}!')
            return redirect('task_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def home(request):
    return render(request, 'home.html')

@login_required
def category_list(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')  # Redirect to the category list view after adding
    else:
        form = CategoryForm()
    
    categories = Category.objects.all()
    return render(request, 'tasks/category_list.html', {'categories': categories, 'form': form})
