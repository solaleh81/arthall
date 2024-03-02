# Importing necessary modules and classes
from django.urls import path  # Module for defining URL patterns
from . import views  # Importing views from the current directory

urlpatterns = [
    # URL pattern for user registration
    path('register/', views.Register.as_view(), name='register'),

    # URL pattern for user login
    path('login/', views.Login.as_view(), name='login'),

    # URL pattern for user logout
    path('logout/', views.Logout.as_view(), name='logout'),

    # URL pattern for user dashboard
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]
