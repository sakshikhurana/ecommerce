from django.db import models
import uuid
import os
from django.http import Http404
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q
# Create your models here.


def upload_image(instance, filename):
    ext = filename.split('.')[-1]
    file = f"{uuid.uuid4()}"
    filename = f'{file}.{ext}'
    return os.path.join('products', f'{file}/{filename}')


class ProductManager(models.Manager):
    def get_object_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().active().search(query)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups).distinct()


class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:slug_detail", kwargs={"slug": self.slug})


# @receiver(presave, sender=models.Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, new_slug=None)


pre_save.connect(product_pre_save_receiver, sender=Product)
