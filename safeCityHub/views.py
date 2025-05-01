from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, emergencyForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Emergencies, Comment
from django.http import JsonResponse
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.core.paginator import Paginator
from bson import ObjectId
import datetime
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import os
from dotenv import load_dotenv
import google.generativeai as genai
from mongoengine.errors import DoesNotExist


load_dotenv()

def emergency_list(request):
    all_emergencies = Emergencies.objects.order_by('-submitted_at')

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        emergency_id = request.POST.get('emergency_id')
        if comment_text and emergency_id:
            emergency = Emergencies.objects(id=emergency_id).first()
            if emergency:
                emergency.comments.append(Comment(text=comment_text))
                emergency.save()
                return redirect(request.path)

    context = {
        'all_emergencies': all_emergencies
    }
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
        GEMINI_KEY = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=GEMINI_KEY)
        


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


        prompt = f"Genarate a ways to mitigate '{incident_type}, with a description of {description} in a small paragraph'"
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        ways_to_mitigate = response.text


        print(response.text)

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
            status=status,
            ways_to_mitigate = ways_to_mitigate
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
def user_profile(request):
    user_obj = request.user

    total_reports = Emergencies.objects.filter(user=user_obj.id).count()
    user_reports_list = Emergencies.objects.filter(user=user_obj.id).order_by('-submitted_at')
    on_going_count = user_reports_list.filter(status='pending').count()

    # GitHub social login info
    try:
        social = SocialAccount.objects.get(user=user_obj)
        github_data = social.extra_data
        avatar_url = github_data.get('avatar_url')
        github_username = github_data.get('login')
    except SocialAccount.DoesNotExist:
        avatar_url = None
        github_username = None

    paginator = Paginator(user_reports_list, 5)
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
    report_count_resolved = Emergencies.objects.filter(status='resolved').count()

    
    print(report_count_resolved, "report count")
    return render(request, 'admin/dashboard.html', {'reports': reports, 'report_count_resolved': report_count_resolved})
    

def analytics(request):
    return render(request, 'admin/analytics.html')



from django.http import HttpResponse
from pymongo import MongoClient
from bson import ObjectId
from gridfs import GridFS



def report_details(request, report_id):
    try:
        report = Emergencies.objects.get(id=ObjectId(report_id))
    except Emergencies.DoesNotExist:
        return render(request, '404.html')

    # Attempt to fetch username from SQLite
    try:
        user = User.objects.get(id=report.user)
        username = user.username
    except User.DoesNotExist:
        username = "Unknown User"

    # Serve proof file if requested
    if request.GET.get('serve_proof'):
        print("serve proof detected")
        try:
            file_id = ObjectId(request.GET.get('serve_proof'))
            client = MongoClient(os.getenv("MONGO_URI"))
            db = client['safecityhub']
            fs = GridFS(db, collection='proofs')
            file = fs.get(file_id)

            if file:
                return HttpResponse(file.read(), content_type=file.content_type)
            else:
                return HttpResponse("Proof not found", status=404)
        except Exception as e:
            print(f"Error accessing proof file: {str(e)}")
            return HttpResponse(f"Error accessing proof file: {str(e)}", status=404)

    # Generate proof URL for viewing
    proof_url = None
    if report.proof:
        try:
            proof_url = f"{request.path}?serve_proof={str(report.proof.grid_id)}"
            print("Generated proof URL:", proof_url)
        except Exception as e:
            print(f"Error accessing proof field: {str(e)}")

    comments = report.comments if hasattr(report, 'comments') else []
    return render(request, 'admin/viewreport.html', {
        'report': report,
        'proof_url': proof_url,
        'username': username,  # Pass to template
        'comments': comments
    })

def update_report(request, report_id):
    try:
        report = Emergencies.objects.get(id=report_id)
    except DoesNotExist:
        raise Http404("Report not found")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            report.status = new_status
            report.save()
            return HttpResponseRedirect(reverse('view_report', args=[str(report.id)]))

    return render(request, 'admin/updatereport.html', {'report': report})

    