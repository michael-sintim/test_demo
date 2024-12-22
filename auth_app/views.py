# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (PasswordChangeForm)
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProfileForm, UserUpdateForm
# from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserUpdateForm


def register(request):
    """
    Handle user registration
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            
            # Log the user in immediately after registration
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {username}!')
                return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def profile_edit(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def change_password(request):
    """
    Allow user to change their password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important! Update the session after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def user_profile(request, username):
    """
    View a user's public profile
    """
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        return render(request, 'profile.html', {
            'viewed_user': user,
            'profile': profile
        })
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('dashboard')
    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
