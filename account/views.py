# Importing necessary modules and classes
from django.contrib import messages, auth  # Module for displaying messages and authentication
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required  # Decorator for login requirement
from django.http import HttpResponse  # Module for HTTP responses
from django.shortcuts import render, redirect  # Functions for rendering templates and redirecting
from django.utils.decorators import method_decorator  # Decorator utility for methods
from rest_framework import status  # Module for HTTP status codes
from rest_framework.views import APIView  # Class-based view for REST framework
from .forms import RegistrationForm  # Importing RegistrationForm from local forms module
from .models import Account  # Importing Account model from local models module

class Register(APIView):
    """
    View class for user registration.

    Methods:
    - get: Handles GET requests for registration page.
    - post: Handles POST requests for user registration form submission.
    """

    def get(self, request):
        """
        Handles GET requests for registration page.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered registration form page.
        """
        form = RegistrationForm()
        return render(request, 'accounts/register.html', context={'form': form})

    def post(self, request):
        """
        Handles POST requests for user registration form submission.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered registration form page with success message if registration is successful,
          otherwise renders registration form page with errors.
        """
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]
            user = Account.object.create_user(first_name=first_name, last_name=last_name,
                                              email=email, username=username,
                                              password=password)
            user.phone_number = phone_number
            user.save()

            messages.success(request, "ثبت نام با موفقیت انجام شد")
            return redirect('register')

        else:
            print(form.errors)
            form = RegistrationForm()
        return render(request, 'accounts/register.html', context={'form': form, 'errors': form.errors})


class Login(APIView):
    """
    View class for user login.

    Methods:
    - get: Handles GET requests for login page.
    - post: Handles POST requests for user login form submission.
    """

    def get(self, request):
        """
        Handles GET requests for login page.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered login page.
        """
        return render(request, 'accounts/login.html')

    def post(self, request):
        """
        Handles POST requests for user login form submission.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Redirects to dashboard page if login is successful, otherwise redirects back to login page
          with error message.
        """
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "با موفقیت وارد حساب کاربری خود شدید")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class Logout(APIView):
    """
    View class for user logout.

    Methods:
    - get: Handles GET requests for user logout.
    """

    def get(self, request):
        """
        Handles GET requests for user logout.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Redirects to login page after successful logout with success message.
        """
        logout(request)
        messages.success(request, "!با موفقیت از حساب کاربری خارج شدید")
        return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class Dashboard(APIView):
    """
    View class for user dashboard.

    Methods:
    - get: Handles GET requests for user dashboard.
    """

    def get(self, request):
        """
        Handles GET requests for user dashboard.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered dashboard page.
        """
        return render(request, "home.html")
