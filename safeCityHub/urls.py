from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView correctly
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('emergencies/', views.map, name='emergencies'),
    path('home/', views.emergency_list, name='home'),
    path('logout/', views.logout_view, name='logout'),  # Point to the custom logout view   
    path('alerts/', views.alerts, name='alerts'),
    path('reports/', views.reports, name='reports'),
    path("report/", views.submitReport, name="submitReport"),
    path("emergencies/getCords/", views.getCords, name="getCords"),
    path('emergency_list/', views.emergency_list, name='emergency_list'),
    path('safecityhub/user/<int:user>/', views.user_profile, name='user'),
    path('about/', views.about, name='about'),
     path('report/<str:pk>/edit/', views.edit_report, name='edit_report'),
    path('report/<str:pk>/delete/', views.delete_report, name='delete_report'),
]
