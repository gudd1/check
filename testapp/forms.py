from django import forms

from testapp.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['CandidateName', 'email', 'password']

    CandidateName    = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Your name:'}))
    email       = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email:'}))
    password    = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password:'}))
