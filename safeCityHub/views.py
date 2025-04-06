from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required   

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'safeCity/login.html', {'form': form})

def map(request):
    return render(request, 'safeCity/map.html')


def logout_view(request):
    # Log the user out
    logout(request)
    
    # Redirect to the login page after logging out
    return redirect('login')

def home(request):
    return render(request, 'safeCity/homepage.html')

def maps(request):
    return render(request, 'safeCity/map.html')

def homepage(request):
    return render(request, 'safeCity/homepage.html')

def alerts(request):
    return render(request, 'safeCity/alerts.html')

# Create your views here.
