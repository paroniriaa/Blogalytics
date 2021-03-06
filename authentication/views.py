from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from .forms import SignupForm, EditProfileForm, ChangePasswordForm, LoginForm
from django.contrib.auth import views as auth_views

# Create your views here.
class UserRegisterView(generic.CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('home')

class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('home')