"""Our forms' test file."""

from django.core import mail
from django.test import TestCase

from ventashop.forms import ContactForm


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

    def test_send_email(self):
        """Check if email is correctly sent."""

        # Act.
        self.contact_form.send_email()  # AttributeError: 'function' object has no attribute 'splitlines'

        # # Assert
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "test_subject")
