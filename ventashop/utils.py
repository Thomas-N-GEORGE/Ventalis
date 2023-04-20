"""A utility module for ventashop app"""

import string, random
from decimal import Decimal

VAT_FRANCE = 0.2

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """Generate a random string of 10 characters"""

    return "".join(random.choice(chars) for i in range(size))


def unique_ref_number_generator(instance):
    """Make unique reference number."""
    ref_number= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(ref_number=ref_number).exists()
    if qs_exists:
        return unique_ref_number_generator(instance)
    return ref_number

def get_VAT_prices(price):
    """
    Calculate VAT and incl. VAT prices from HT price.
    
    Args:
        price (Decimal): price VAT excl.
        
    Returns:
        vat_amount (Decimal),
        incl_vat_price (Decimal).
    """

    vat = Decimal(VAT_FRANCE)
    vat_amount = (vat * price)
    incl_vat_price = ((1 + vat) * price)

    return vat_amount, incl_vat_price
