from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model


User = get_user_model()
non_allowed_words = 'hack'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    ip_address = forms.CharField(widget=forms.HiddenInput)




class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=40,required=False,help_text='optional')
    last_name = forms.CharField(max_length=40,required=False,help_text='optional')
    birthday = forms.DateField(required=False,help_text='optional format: yyyy-MM--DD')
    email = forms.CharField(max_length=120,help_text='Required Submit a valid email address')
    class Meta:
        model = User
        fields = ('username','first_name','last_name','birthday','email','password1','password2',)



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthday',)