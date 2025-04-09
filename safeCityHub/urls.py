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
]
