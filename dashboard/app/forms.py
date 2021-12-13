from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')
        widgets = {
            'Username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'placeholder':'Register username'}),
             'password': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'placeholder':'Create Password'}),   
             'password2': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'placeholder':'Confirm Password'}),  
        }
class LoginForm(forms.ModelForm):
    '''Simple login form'''
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'placeholder':'Enter username'}),
             'password': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'placeholder':'Enter Password'}),     
        }