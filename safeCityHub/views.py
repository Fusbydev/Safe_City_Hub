from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, emergencyForm
from django.contrib.auth.decorators import login_required
from .models import Emergencies
from django.http import JsonResponse

def emergency_list(request):
    # Retrieve all emergencies from the database
    all_emergencies = Emergencies.objects.all()

    # Debugging: Print the data to the console/log
    print("All Emergencies:", all_emergencies)

    # Correct way to pass the context: it must be a dictionary
    context = {
        'all_emergencies': all_emergencies,
    }

    # Render the template with the correct context
    return render(request, 'safeCity/homepage.html', context)


def getCords(request):
    cords = list(Emergencies.objects.values_list('latitude', 'longitude'))
    print(cords)
    return JsonResponse({'cords': cords})

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


def submitReport(request):
    if request.method == "POST":
        incident_type = request.POST.get("incident-type")
        urgency_level = request.POST.get("urgency-level")
        date = request.POST.get("date")
        contact_number = request.POST.get("contact-number")
        description = request.POST.get("description")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        anonymous = request.POST.get("anonymous") == "on"
        proof = request.FILES.get("proof")

        report = Emergencies.objects.create(
            incident_type=incident_type,
            urgency_level=urgency_level,
            date=date,
            contact_number=contact_number,
            description=description,
            longitude=longitude,
            latitude=latitude,
            anonymous=anonymous,
            proof=proof
        )
        return redirect("reports")  # Make a success page or redirect

    return render(request, "submit_form.html")  # Your HTML form file


# routing
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

def reports(request):
    return render(request, 'safeCity/reports.html')

# Create your views here.
