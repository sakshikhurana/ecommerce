from django.utils.text import slugify
import random
import string


def random_string_generator(size=10, char=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def unique_order_id_generator(instance):
    new_order_id = random_string_generator()
    kclass = instance.__class__
    qs = kclass.objects.filter(order_id=new_order_id).exists()
    if qs:
        return unique_order_id_generator(instance)
    return new_order_id
