from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Todo

@csrf_exempt
def signup_view(request):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST method allowed'},
            status=405
        )

    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if not username or not password1 or not password2:
        return JsonResponse(
            {'error': 'All fields are required'},
            status=400
        )

    if password1 != password2:
        return JsonResponse(
            {'error': 'Passwords do not match'},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {'error': 'Username already exists'},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password1
    )

    login(request, user)

    return JsonResponse(
        {'message': 'User created successfully'},
        status=201
    )

@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST method allowed'},
            status=405
        )

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return JsonResponse(
            {'error': 'Username and password required'},
            status=400
        )

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse(
            {'error': 'Invalid credentials'},
            status=401
        )

    login(request, user)

    return JsonResponse(
        {'message': 'Login successful'},
        status=200
    )


@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)

    data = []
    for todo in todos:
        data.append({
            'id': todo.id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo.created_at
        })

    return JsonResponse(
        {'todos': data},
        status=200
    )

@csrf_exempt
@login_required
def add_todo(request):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST method allowed'},
            status=405
        )

    title = request.POST.get('title')

    if not title:
        return JsonResponse(
            {'error': 'Title is required'},
            status=400
        )

    todo = Todo.objects.create(
        user=request.user,
        title=title
    )

    return JsonResponse(
        {
            'message': 'Todo created successfully',
            'todo_id': todo.id,
            'title': todo.title,
            'completed': todo.completed
        },
        status=201
    )

@csrf_exempt
@login_required
def delete_todo(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        todo = Todo.objects.get(id=id, user=request.user)
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)

    todo.delete()

    return JsonResponse({'message': 'Todo deleted'}, status=200)



@csrf_exempt
@login_required
def toggle_todo(request, id):
    if request.method != 'PATCH':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        todo = Todo.objects.get(id=id, user=request.user)
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)

    todo.completed = not todo.completed
    todo.save()

    return JsonResponse({
        'id': todo.id,
        'completed': todo.completed
    }, status=200)

