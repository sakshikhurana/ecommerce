from django.shortcuts import render, redirect
from billing.models import BillingProfile
from .forms import AddressForm
from django.utils.http import is_safe_url

# Create your views here.

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {'form': form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile:
            instance.billing_profile = billing_profile
            instance.address_types = request.POST.get('address_type', 'shipping')
            instance.save()
        else:
            print('Error here')
            return redirect('cart:checkout')
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('cart:checkout')
    return redirect('cart:checkout')
