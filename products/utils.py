from django.utils.text import slugify
import random
import string


def random_string_generator(size=10, char=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    kclass = instance.__class__
    qs = kclass.objects.filter(slug=slug).exists()
    if qs:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug)
    return slug
