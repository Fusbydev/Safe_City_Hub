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
    path('safecityhub/user/profile/', views.user_profile, name='user_profile'),
    path('about/', views.about, name='about'),
    path('report/<str:pk>/edit/', views.edit_report, name='edit_report'),
    path('report/<str:pk>/delete/', views.delete_report, name='delete_report'),
    path('register/', views.register, name='register'),
    path("admin/", views.admin, name="admin"),
    path("analytics/", views.analytics, name="analytics"),
    path('view_report/<str:report_id>/', views.report_details, name='view_report'),
    path('update_report/<str:report_id>/', views.update_report, name='update_report'),
    path('tags/<str:tag>/', views.emergencies_by_tags, name='tagged_emergencies'),
    path('update_profile/<int:user_id>/', views.update_profile, name='update_profile'),
]
