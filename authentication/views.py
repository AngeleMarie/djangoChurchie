from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib import messages
from django.contrib import auth

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '')
        validator = EmailValidator()

        try:
            validator(email)
        except ValidationError:
            return JsonResponse({'email_error': 'Invalid email address.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is already in use.'}, status=409)

        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username', '')

        if not username:
            return JsonResponse({'username_error': 'Username cannot be empty.'}, status=400)

        if not username.isalnum():
            return JsonResponse({'username_error': 'Username should contain only alphanumeric characters.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already in use.'}, status=409)

        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        church=request.POST.get('church')

        context = {'fieldValues': request.POST}

        # Input validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True  # Directly activate the user
            user.save()

            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')

        return render(request, 'authentication/register.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username and password:
            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome, {user.username}!')
                    return redirect('christians')  # Replace with actual redirect target
                messages.error(request, 'Account is not active. Please contact support.')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')

        else:
            messages.error(request, 'Please provide both username and password.')

        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')
