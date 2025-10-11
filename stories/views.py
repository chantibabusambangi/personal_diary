from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Story
import requests
import os

def home(request):
    stories = Story.objects.filter(visibility='public').order_by('-created_at')
    return render(request, 'home.html', {'stories': stories})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def profile(request):
    stories = Story.objects.filter(author=request.user).order_by('-created_at')
    
    # Call Flask API for analytics
    flask_url = os.environ.get('FLASK_URL', 'http://localhost:5000')
    analytics = {}
    try:
        response = requests.get(f'{flask_url}/api/analytics', timeout=2)
        if response.status_code == 200:
            analytics = response.json()
    except:
        analytics = {'message': 'Analytics service unavailable'}
    
    context = {
        'stories': stories,
        'analytics': analytics,
        'total_stories': stories.count(),
        'public_stories': stories.filter(visibility='public').count()
    }
    return render(request, 'profile.html', context)

@login_required
def create_story(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        visibility = request.POST.get('visibility', 'private')
        
        Story.objects.create(
            author=request.user, 
            title=title, 
            content=content, 
            visibility=visibility
        )
        messages.success(request, 'Story created successfully!')
        return redirect('profile')
    
    return render(request, 'create.html')