from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Username", 'name': "username", 'maxlength': "100",  'id': "id_username"}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "First Name", 'name': "firstname", 'maxlength': "100",  'id': "id_first_name"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Last Name", 'name': "lastname", 'maxlength': "100",  'id': "id_last_name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': "email", 'placeholder': "Email", 'name': "email", 'maxlength': "100", 'required': True, 'id': "id_email"}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': "Password", 'name': "new password", 'maxlength': "100", 'required': True, 'id': "id_new_password1"}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': "Password Confirmation", 'name': "new password confirmation", 'maxlength': "100", 'required': True, 'id': "id_new_password2"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Username", 'name': "username", 'maxlength': "100",  'id': "id_username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': "email", 'placeholder': "Email", 'name': "email", 'maxlength': "100", 'required': True, 'id': "id_email"}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "First Name", 'name': "firstname", 'maxlength': "100",  'id': "id_first_name"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Last Name", 'name': "lastname", 'maxlength': "100",  'id': "id_last_name"}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': "Current Password", 'name': "current password", 'maxlength': "100", 'required': True, 'id': "id_old_password"}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': "New Password", 'name': "new password", 'maxlength': "100", 'required': True, 'id': "id_new_password1"}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': "New Password Confirmation", 'name': "new password confirmation", 'maxlength': "100", 'required': True, 'id': "id_new_password2"}))
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2',)

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Username", 'name': "username", 'maxlength': "100",  'id': "id_username"}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': "Password", 'name': "password", 'maxlength': "100", 'required': True, 'id': "id_password"}))
    class Meta:
        model = User
        fields = ['username', 'password']