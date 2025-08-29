from django import forms
from django.contrib.auth.models import User
from .models import Indicator

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = "__all__"

        widgets = {
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}),
            "indicator": forms.TextInput(attrs={"class": "form-control", "placeholder": "Indicator"}),
            "year": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Year"}),
            "value": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Value"}),
        }

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data
