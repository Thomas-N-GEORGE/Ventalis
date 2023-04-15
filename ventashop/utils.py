"""A utility module for ventashop app"""

import string
import random


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for i in range(size))


def unique_ref_number_generator(instance):
    ref_number= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(ref_number=ref_number).exists()
    if qs_exists:
        return unique_ref_number_generator(instance)
    return ref_number