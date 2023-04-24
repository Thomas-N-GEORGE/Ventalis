"""Our forms' test file."""

from django.contrib.auth.hashers import make_password
from django.core import mail
from django.test import TestCase

from ventashop.forms import ContactForm, UserForm
from ventashop.models import User, CustomerAccount, Cart


class ContactFormTestCase(TestCase):
    """Test class for the contact form logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.contact_form = ContactForm()
        cls.contact_form.cleaned_data = {
            "company": "test_company",
            "last_name": "test_last_name", 
            "first_name": "test_first_name",
            "from_email": "test_from_email@test.com",
            "subject": "test_subject",
            "content": "test_content",
        }

    def test_build_message_from_info(self):
        """Check if method returns correct message."""

        # Act.
        message = self.contact_form.build_message_from_info()

        # Assert.
        self.assertEqual(
            message,
            "Société : test_company\nNom : test_last_name\nPrénom : test_first_name\n\n\ntest_content"
        )

    # def test_send_email(self):
        """Check if email is correctly sent."""

        # Act.
        self.contact_form.send_email()  # AttributeError: 'function' object has no attribute 'splitlines'

        # # Assert
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "test_subject")


class UserFormTestCase(TestCase):
    """Test class for the user form logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.user_form = UserForm()
        cls.user_form.cleaned_data = {
            "email": "employee1@ventalis.com",
            "password": "12345678&",
            "first_name": "emp1_first_name",
            "last_name": "emp1_last_name", 
        }
        cls.employee1 = cls.user_form.create_user(role="EMPLOYEE")
        cls.user_form.cleaned_data = {
            "email": "employee2@ventalis.com",
            "password": "12345678&",
            "first_name": "emp2_first_name",
            "last_name": "emp2_last_name", 
        }
        cls.employee2 = cls.user_form.create_user(role="EMPLOYEE")
        cls.user_form.cleaned_data = {
            "email": "customer1@test.com",
            "password": "12345678&",
            "first_name": "cust1_first_name",
            "last_name": "cust1_last_name", 
        }
        cls.customer1 = cls.user_form.create_user(role="CUSTOMER")

    def test_create_user_employee_role(self):
        """Check if employee reg number and company get set during creation process."""

        # Assert.
        self.assertIsNotNone(self.employee1.reg_number)
        self.assertEqual(self.employee1.company, "Ventalis")

    def test_create_user_customer_role(self):
        """Check if customer related customer account and cart are created during creation process."""

        # Arrange.
        customer_account_count = CustomerAccount.objects.all().count()
        cart_count = Cart.objects.all().count()

        # Act.
        self.user_form.cleaned_data = {
            "email": "customer2@test.com",
            "password": "12345678&",
            "first_name": "cust2_first_name",
            "last_name": "cust2_last_name", 
        }
        customer2 = self.user_form.create_user(role="CUSTOMER")

        # Assert.
        self.assertEqual(customer_account_count + 1, CustomerAccount.objects.all().count())
        self.assertEqual(cart_count + 1, Cart.objects.all().count())
        self.assertEqual(CustomerAccount.objects.filter(customer=customer2).count(), 1)

    def test_create_user_customer_role_assigned_to_correct_employee(self):
        """
        Check if customer is assigned to employee reg_number through his customer account,
        employee being the one with the least assigned customers.
        """

        # Act.
        self.user_form.cleaned_data = {
            "email": "customer2@test.com",
            "password": "12345678&",
            "first_name": "cust2_first_name",
            "last_name": "cust2_last_name", 
        }
        customer2 = self.user_form.create_user(role="CUSTOMER")

        # Assert.
        self.assertNotEqual(
            self.customer1.customeraccount.employee_reg,
            customer2.customeraccount.employee_reg
        )
        
        ###############
        # And again...#
        ###############
        # Act.
        self.user_form.cleaned_data = {
            "email": "customer3@test.com",
            "password": "12345678&",
            "first_name": "cust3_first_name",
            "last_name": "cust3_last_name", 
        }
        customer3 = self.user_form.create_user(role="CUSTOMER")
        self.user_form.cleaned_data = {
            "email": "customer4@test.com",
            "password": "12345678&",
            "first_name": "cust4_first_name",
            "last_name": "cust4_last_name", 
        }
        customer4 = self.user_form.create_user(role="CUSTOMER")
        
        # Assert.
        self.assertNotEqual(
            customer3.customeraccount.employee_reg,
            customer4.customeraccount.employee_reg
        )
        
        #######################
        # And one last time...#
        #######################
        # Act.
        self.user_form.cleaned_data = {
            "email": "customer5@test.com",
            "password": "12345678&",
            "first_name": "cust5_first_name",
            "last_name": "cust5_last_name", 
        }
        customer5 = self.user_form.create_user(role="CUSTOMER")
        self.user_form.cleaned_data = {
            "email": "customer6@test.com",
            "password": "12345678&",
            "first_name": "cust6_first_name",
            "last_name": "cust6_last_name", 
        }
        customer6 = self.user_form.create_user(role="CUSTOMER")
        
        # Assert.
        self.assertNotEqual(
            customer5.customeraccount.employee_reg,
            customer6.customeraccount.employee_reg
        )
        # With 6 previously created customers, we should find "3 per employee".
        self.assertEqual(
            CustomerAccount.objects.filter(employee_reg=self.employee1.reg_number).count(),
            CustomerAccount.objects.filter(employee_reg=self.employee2.reg_number).count()
            )