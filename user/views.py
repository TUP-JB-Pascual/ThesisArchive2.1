from django.shortcuts import render, redirect, resolve_url
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterUserForm, UpdateProfileForm, ChangePasswordForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse

import random
import string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.conf import settings

def UserRegisterView(request):
    if request.user.is_authenticated:
        messages.success(request, "To Access the Registration Page, you need to log out first.")
        return redirect('home')
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password1']
            User = get_user_model()
            
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect('user_registration')
            
            # Create the user (but don't activate them yet)
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            user.is_active = False
            user.save()

            # Generate the token
            token = default_token_generator.make_token(user)

            # Send verification email
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())
            current_site = get_current_site(request)
            verification_url = f"{current_site.domain}/user/verify-email/{uidb64}/{token}/"
            
            subject = 'Verify your email address'
            message = (f"Hello {first_name} {last_name},\n\n"
                "Thank you for registering on our website.\n\n"
                "Please click the following link to verify your email address and activate your account:\n\n"
                f"{verification_url}\n\n"
                "If you did not register, please ignore this email.\n\n"
                "Best regards,\nYour Team")
            send_mail(subject, message, 'no-reply@tupcthesisarchive.com', [email])
            
            messages.success(request, 'A verification email has been sent to your email address. Please check SPAM folder.')
            return redirect('user_registration')  # Redirect to some "check your email" page
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})

def VerifyEmail(request, uidb64, token):
    try:
        # Decode the user ID from the base64 string
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate the user account
        user.save()
        messages.success(request, 'Your email has been successfully verified. Please login.')
        return redirect('login')  # Redirect to success page after successful verification
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('user_registration')  # Redirect back to registration if the link is invalid

class UserLoginView(LoginView):
    redirect_authenticated_user=True
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated and self.redirect_authenticated_user:
            # Redirect to a different view if user is authenticated
            messages.success(self.request, "To Access the Login Page, you need to log out first.")
            return redirect(reverse('home'))

        # Proceed with the normal view processing if not authenticated
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            messages.success(self.request, "Welcome Super User")
            return reverse_lazy('home')
        elif self.request.user.is_authenticated:
            messages.success(self.request, "Welcome User")
            return reverse_lazy('home') 
        else:
            messages.success(self.request, "To access that page you need to log in.")
            return reverse_lazy('login') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
class UserLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('login')

@login_required
def UserProfile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile/profile.html', context)

@login_required
def UserUpdateProfile(request):
    if request.user.is_authenticated:
        User = get_user_model()
        current_user = User.objects.get(id=request.user.id)
        form = UpdateProfileForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "You've successfully update your profile.")
            return redirect('user_profile')
        context = {'form': form}
        return render(request, 'profile/change_profile.html', context)
    else:
        messages.success(request, "You must be logged in to access that page.")
        return redirect('login')

@login_required
def UserChangePassword(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            pass
        else:
            form = ChangePasswordForm(current_user)
            context ={'form': form}
            return render(request, 'profile/change_password.html', context)
    else:
        messages.success(request, "To Access this page you need to log in first.")
        return redirect('login')

def UserForgotPassword(request):
    pass
