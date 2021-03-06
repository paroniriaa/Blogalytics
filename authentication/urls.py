from . import views
from django.urls import path
from .views import UserRegisterView, PasswordChangeView, UserLoginView
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('password/', PasswordChangeView.as_view(template_name='registration/change-password.html')),
]