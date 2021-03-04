from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed, pre_save
# Create your models here.

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if not user_obj:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() != 1:
            # cart_obj = cart_create(request)
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
            new_obj = True
        else:
            print('Cart id exists')
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        print(cart_obj)
        return cart_obj, new_obj


class Cart(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
