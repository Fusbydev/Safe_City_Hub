from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, emergencyForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Emergencies
from django.http import JsonResponse
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.core.paginator import Paginator
from bson import ObjectId
import datetime
from django.http import Http404
from django.contrib import messages



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


def alerts(request):

    incident_type = request.GET.get('incident_type')
    if incident_type:
        alerts = Emergencies.objects.filter(incident_type=incident_type)
    else:
        alerts = Emergencies.objects.all()
    
    return render(request, 'safeCity/alerts.html', {'alerts': alerts, 'incident_type': incident_type})



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
    submitted = False

    if request.method == "POST":
        # Get form data
        incident_type = request.POST.get("incident-type")
        urgency_level = request.POST.get("urgency-level")
        date_str = request.POST.get("date")  # Date as a string
        contact_number = request.POST.get("contact-number")
        description = request.POST.get("description")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        anonymous = request.POST.get("anonymous") == "on"
        proof = request.FILES.get("proof")
        address = request.POST.get("location")
        status = "pending"

        # Convert date string to datetime object
        try:
            date = datetime.datetime.fromisoformat(date_str)  # Convert to datetime
        except ValueError:
            # Handle invalid date format if necessary
            date = None  # or raise an error

        # Convert longitude and latitude to float
        try:
            longitude = float(longitude)
            latitude = float(latitude)
        except ValueError:
            # Handle invalid float if necessary
            longitude = 0.0
            latitude = 0.0

        # Create a report, passing the user as an ObjectId
        report = Emergencies.objects.create(
            user=request.user.id,  # ✅ Just use the int
            incident_type=incident_type,
            urgency_level=urgency_level,
            date=date,
            contact_number=contact_number,
            description=description,
            longitude=longitude,
            latitude=latitude,
            anonymous=anonymous,
            proof=proof,
            address = address,
            status=status
        )
        submitted = True

    return render(request, "safeCity/reports.html", {'submitted': submitted})


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

@login_required
def reports(request):
    return render(request, 'safeCity/reports.html')


def about(request):
    return render(request, 'safeCity/about.html')

# Create your views here.


@login_required
def user_profile(request, user):
    # Get the User object from the Django User model
    user_obj = get_object_or_404(User, id=user)
    #convert user_obj to string
    

    # Query the Emergencies collection using ObjectId to match the user reference
    total_reports = Emergencies.objects.filter(user=user_obj.id).count()  # Ensure we query with ObjectId

    # Fetch the social account linked with the user (make sure this user has one)
    try:
        social = SocialAccount.objects.get(user=user_obj)
        github_data = social.extra_data
        avatar_url = github_data.get('avatar_url')
        github_username = github_data.get('login')
    except SocialAccount.DoesNotExist:
        avatar_url = None
        github_username = None

    # User's reports - query by the user reference (ensure we use ObjectId here)
    user_reports_list = Emergencies.objects.filter(user=user_obj.id).order_by('-submitted_at')
    on_going_count = user_reports_list.filter(status='pending').count()

    # Pagination setup
    paginator = Paginator(user_reports_list, 5)  # Show 5 reports per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'safeCity/user.html', {
        'user_obj': user_obj,
        'avatar_url': avatar_url,
        'github_username': github_username,
        'page_obj': page_obj,
        'total_reports': total_reports,
        'on_going_count': on_going_count
    })
def edit_report(request, pk):
    # logic to handle editing a report
    pass

def delete_report(request, pk):
    try:
        report = Emergencies.objects.get(id=ObjectId(pk))
    except (Emergencies.DoesNotExist, ValueError):
        raise Http404("Report not found")

    report.delete()
    return redirect('user', user=str(request.user.id))  # ensure user ID is passed as a string



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # redirect to your login page
    else:
        form = RegisterForm()
    return render(request, 'safeCity/register.html', {'form': form})

@login_required
def admin(request):

    if not request.user.is_superuser:
        return redirect('home')
    
    reports = Emergencies.objects.all()

    return render(request, 'admin/dashboard.html', {'reports': reports})

def analytics(request):
    return render(request, 'admin/analytics.html')




