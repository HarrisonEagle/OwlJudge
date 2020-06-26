from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())