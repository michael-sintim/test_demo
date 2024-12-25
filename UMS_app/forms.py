from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=False
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'bio', 
            'birth_date'
        ]

class UserUpdateForm(UserChangeForm):
    password = None  # Remove password field from update form

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'birth_date']