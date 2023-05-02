"""Our view's authorization/redirection test module."""

from django.test import Client, TestCase
from ventashop.tests import utils_tests
from ventashop.models import Conversation


class AllViewsRedirectionTestCase(TestCase):
    """Test class for redirection in views."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.administrator = utils_tests.create_administrator()
        cls.employee1 = utils_tests.create_employee1()
        cls.customer1 = utils_tests.create_customer1()
        cls.empl1_pk = cls.employee1.pk
        cls.conv_id = Conversation.objects.filter(participants=cls.customer1).filter(participants=cls.employee1)[0].pk
        cls.c = Client()

    def test_customer_authorization(self):
        """Test case for customer authorization in views."""

        # Arrange.
        self.c.login(email='customer1@test.com', password='12345678&')


        # Act.
        response1 = self.c.get(path="/my_space/")
        response2 = self.c.get(path="/cart/")
        response3 = self.c.get(path="/orders/")
        response4 = self.c.get(path="/conversations/")
        # response5 = self.c.get(path="/messages/")
        response6 = self.c.get(path="/" + str(self.conv_id) + "/messages/")
        response7 = self.c.get(path="/" + str(self.conv_id) + "/messages/5")
        response8 = self.c.get(path="/intranet/")
        response9 = self.c.get(path="/customers/")
        response10 = self.c.get(path="/product_form/")
        response11 = self.c.get(path="/category_form/")
        response12 = self.c.get(path="/administration/employees/")
        response13 = self.c.get(path="/administration/employee_create/")
        response14 = self.c.get(path="/administration/" + str(self.empl1_pk) + "/employee_update/")

        # Assert.
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response4.status_code, 403)
        # self.assertEqual(response5.status_code, 200)
        self.assertEqual(response6.status_code, 200)
        self.assertEqual(response7.status_code, 200)
        self.assertEqual(response8.status_code, 403)
        self.assertEqual(response9.status_code, 403)
        self.assertEqual(response10.status_code, 403)
        self.assertEqual(response11.status_code, 403)
        self.assertEqual(response12.status_code, 403)
        self.assertEqual(response13.status_code, 403)
        self.assertEqual(response14.status_code, 403)

        self.c.logout()

    def test_employee_authorization(self):
        """Test case for employee authorization in views."""

        # Arrange.
        self.c.login(email='employee1@ventalis.com', password='12345678&')

        # Act.
        response1 = self.c.get(path="/my_space/")
        response2 = self.c.get(path="/cart/")
        response3 = self.c.get(path="/orders/")
        response4 = self.c.get(path="/conversations/")

        response8 = self.c.get(path="/intranet/")
        response9 = self.c.get(path="/customers/")
        response10 = self.c.get(path="/product_form/")
        response11 = self.c.get(path="/category_form/")
        response12 = self.c.get(path="/administration/employees/")
        response13 = self.c.get(path="/administration/employee_create/")
        response14 = self.c.get(path="/administration/" + str(self.empl1_pk) + "/employee_update/")

        # Assert.
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(response4.status_code, 200)

        self.assertEqual(response8.status_code, 200)
        self.assertEqual(response9.status_code, 200)
        self.assertEqual(response10.status_code, 200)
        self.assertEqual(response11.status_code, 200)
        self.assertEqual(response12.status_code, 403)
        self.assertEqual(response13.status_code, 403)
        self.assertEqual(response14.status_code, 403)

        self.c.logout()

    
    def test_administrator_authorization(self):
        """Test case for employee authorization in views."""

        # Arrange.
        self.c.login(email='administrator@ventalis.com', password='12345678&')

        # Act.
        response1 = self.c.get(path="/my_space/")
        response2 = self.c.get(path="/cart/")
        response3 = self.c.get(path="/orders/")
        response4 = self.c.get(path="/conversations/")

        response8 = self.c.get(path="/intranet/")
        response9 = self.c.get(path="/customers/")
        response10 = self.c.get(path="/product_form/")
        response11 = self.c.get(path="/category_form/")
        response12 = self.c.get(path="/administration/employees/")
        response13 = self.c.get(path="/administration/employee_create/")
        response14 = self.c.get(path="/administration/" + str(self.empl1_pk) + "/employee_update/")

        # Assert.
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(response4.status_code, 403)

        self.assertEqual(response8.status_code, 403)
        self.assertEqual(response9.status_code, 403)
        self.assertEqual(response10.status_code, 403)
        self.assertEqual(response11.status_code, 403)
        self.assertEqual(response12.status_code, 200)
        self.assertEqual(response13.status_code, 200)
        self.assertEqual(response14.status_code, 200)

        self.c.logout()
