from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
        required=True,
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter password", "class": "form-control"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm password", "class": "form-control"}
        )
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    # We use username instead of email here due to django
    # expecting the login field to be named username
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
        required=True,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter password", "class": "form-control"}
        )
    )

    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Current Password", "class": "form-control"}
        ),
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "New Password", "class": "form-control"}
        ),
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm New Password", "class": "form-control"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password1", "new_password2"]


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label="Email Address", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    first_name = forms.CharField(
        label="First Name", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="Last Name", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name"]
