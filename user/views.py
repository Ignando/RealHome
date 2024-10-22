from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import CustomUser
from django.urls import reverse
from main.models import Property  
import logging

# Set up logger for debugging
logger = logging.getLogger(__name__)

# Home View
def home(request):
    return render(request, 'home.html')

# Login View
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        logger.info(f"Login attempt for username: {username}")

        # Validate input
        if not username or not password:
            logger.warning("Login attempt with missing username or password")
            return JsonResponse({'success': False, 'message': 'Username and password are required.'}, status=400)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"Successful login for username: {username}")
            return JsonResponse({'success': True, 'redirect_url': reverse('auth:dashboard')})
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

# Register View
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'GET':
        return render(request, 'auth/register.html')

    elif request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            user_type = request.POST.get('userType')
            license_number = request.POST.get('licenseNumber')

            # Validate input data
            if not all([name, email, password, phone, user_type]):
                return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'success': False, 'message': 'Invalid email address.'}, status=400)

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already in use.'}, status=400)

            if user_type not in ['customer', 'realtor']:
                return JsonResponse({'success': False, 'message': 'Invalid user type.'}, status=400)

            if user_type == 'realtor' and not license_number:
                return JsonResponse({'success': False, 'message': 'License number is required for realtors.'}, status=400)

            # Create new user
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name.split()[0],
                last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                phone=phone,
                user_type=user_type,
                license_number=license_number if user_type == 'realtor' else None
            )

            # Log user in after successful registration
            login(request, user)

            # Return success response
            return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})

        except Exception as e:
            # Log the exception for server-side debugging
            logger.error(f"Error in register_view: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred. Please try again.'}, status=500)

    # This line should never be reached due to @require_http_methods, but keep it for completeness
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


# Dashboard View
@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'total_properties': Property.objects.filter(owner=user).count(),
        'recent_properties': Property.objects.filter(owner=user).order_by('-created_at')[:5],
        'property_types': Property.objects.filter(owner=user).values('property_type').annotate(count=Count('property_type')),
    }
    return render(request, 'dashboard.html', context)
