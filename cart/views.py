from django.shortcuts import render, redirect
from .models import Cart
from order.models import Order
from products.models import Product
from billing.models import BillingProfile
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
# Create your views here.


def cart_create(request):
    cart_obj = Cart.objects.create(user=None)
    print('New Cart Created')
    return cart_obj


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    request.session['cart_items'] = cart_obj.products.count()
    return render(request, 'cart/home.html', {'cart': cart_obj})


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('Product is out of stock')
            return redirect('cart:home')

        cart_obj, _ = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
    return redirect('cart:home')


def checkout_home(request):
    order_obj = None
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile=billing_profile, cart_obj=cart_obj)

    context = {'object': order_obj, 'billing_profile': billing_profile,
               'login_form': login_form, 'guest_form': guest_form,
               'address_form': address_form,
               'billing_address_form': billing_address_form}
    return render(request, 'cart/checkout.html', context)
