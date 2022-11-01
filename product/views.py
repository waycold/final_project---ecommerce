from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db import IntegrityError


def home(request):
    return render(request, 'home.html')

# sign up function

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'User already exists'})
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'})


# log out function

def log_out(request):
    logout(request)
    return redirect('home')


# log in function

def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
        'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html',{
            'form': AuthenticationForm, 
            'error': 'User or password is incorrect'})
        else:
            login(request, user)
            return redirect('home')
