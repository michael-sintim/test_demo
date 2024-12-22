# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile
    """
    class Meta:
        model = Profile
        fields = [
            # 'bio', 
            'birth_date', 
             
           ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            # 'bio': forms.Textarea(attrs={'rows': 4}),
        }

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']