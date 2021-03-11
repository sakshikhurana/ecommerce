from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.http import is_safe_url
from django.conf import settings
# Create your views here.


def login_page(request):
    form = forms.LoginForm(request.POST or None)
    context = {'form': form}
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('Logged in')
            login(request, user=user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            print('Error')
    return render(request, 'accounts/auth/login.html', context)


def register_page(request):
    form = forms.RegisterForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(
            username=username, password=password, email=email)
        print(new_user)
    return render(request, 'accounts/auth/register.html', context)


# def contact_page(request):
#     contact_form = ContactForm(request.POST or None)
#     if contact_form.is_valid():
#         print(contact_form.cleaned_data)

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if 'gmail' not in email:
#             raise forms.ValidationError('Email not correct')
#         return email
