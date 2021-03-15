from django.db import models
from cart.models import Cart
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from math import fsum
from billing.models import BillingProfile
# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'), ('refunded', 'Refunded'),
    ('paid', 'Paid'), ('shipped', 'Shipped'),)

class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        qs = Order.objects.filter(
            billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:
            order_obj = qs.first()
            created = False
        else:
            order_obj = Order.objects.create(
                billing_profile=billing_profile, cart=cart_obj)
            created = True
        return order_obj, created

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created',
                              choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(
        default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = fsum([cart_total, shipping_total])
        self.total = new_total
        self.save()
        return self.total

    def __str__(self):
        return self.order_id


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order_total(sender, instance, created, *args, **kwargs):
    print('running')
    if created:
        print('updating')
        instance.update_total()


post_save.connect(post_save_order_total, sender=Order)


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)
