from django.shortcuts import render, redirect
from .models import Cart
from order.models import Order
from products.models import Product
from billing.models import BillingProfile
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
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
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(
                billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile=billing_profile, cart_obj=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(
                id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(
                id=billing_address_id)
            del request.session['billing_address_id']
    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect('cart:success')
    if billing_address_id or shipping_address_id:
        order_obj.save()

    context = {'object': order_obj, 'billing_profile': billing_profile,
               'login_form': login_form, 'guest_form': guest_form,
               'address_form': address_form, 'address_qs': address_qs,
               'billing_address_form': billing_address_form}
    return render(request, 'cart/checkout.html', context)


def checkout_done_view(request):
    return render(request, "cart/checkout-done.html", {})
