from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.http import is_safe_url
from django.conf import settings
from .models import GuestEmail
from django.views.generic import FormView, CreateView
# Create your views here.


class LoginView(FormView):
    form_class = forms.LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        import pdb
        pdb.set_trace()
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            # if not user.is_active:
            #     print('inactive user..')
            #     messages.success(request, "This user is inactive")
            #     return super(LoginView, self).form_invalid(form)
            login(request, user)
            # user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super().form_invalid(form)
    # def form_valid(self, form):
    #     next_path = self.get_next_url()
    #     return redirect(next_path)


class RegisterView(CreateView):
    form_class = forms.RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'
# def contact_page(request):
#     contact_form = ContactForm(request.POST or None)
#     if contact_form.is_valid():
#         print(contact_form.cleaned_data)

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if 'gmail' not in email:
#             raise forms.ValidationError('Email not correct')
#         return email


def guest_register_page(request):
    form = forms.GuestForm(request.POST or None)
    context = {'form': form}
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return render(request, 'accounts/auth/register.html', context)
