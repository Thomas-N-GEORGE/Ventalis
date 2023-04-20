"""This is our tests file for module utils.py"""

from decimal import Decimal

from django.test import TestCase

from ventashop.utils import get_VAT_prices


class UtilsTestCase(TestCase):
    """Test class for functions in utils.py module."""

    def test_get_VAT_prices(self):
        """Check get_VAT_prices calculations"""

        # Arrange.
        price = Decimal(100)

        # Act.
        vat_amount, incl_vat_price = get_VAT_prices(price=price)
    
        # Assert.
        self.assertEqual(vat_amount, price * Decimal(0.2))
        self.assertEqual(incl_vat_price, price * (1 + Decimal(0.2)))
