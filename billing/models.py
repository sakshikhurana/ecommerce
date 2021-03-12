from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(
            user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)

# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.customer_id = newID
#         instance.save()