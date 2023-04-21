"""
The file containing all our forms
Unused at this time
"""

from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm

from ventashop.models import Category
from ventasite.settings import VENTALIS_EMAIL


# class CategoryForm(forms.Form):
#     name = forms.CharField(label="Nom de la catégorie", max_length=200)


# Will display an automatic message if failed to create object.
# 
# class CategoryForm(ModelForm):
#     class Meta:
#         model = Category
#         fields = ["name"]


class Form(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class MessageForm(forms.Form):
    """Our new message form."""

    content = forms.CharField(label="Nouveau message")


class ContactForm(forms.Form):
    """Our email form class, for the contact view."""

    company = forms.CharField(label="Nom de la société")
    last_name = forms.CharField(label="Nom")
    first_name = forms.CharField(label="Prénom")
    from_email = forms.EmailField(label="Email")
    subject = forms.CharField(label="Objet")
    content = forms.CharField(label="Description", widget=forms.Textarea)

    def build_message_from_info(self) -> str:
        """Build content from data."""

        company_info = "Société : " + self.cleaned_data["company"]
        last_name_info = "Nom : " + self.cleaned_data["last_name"]
        first_name_info = "Prénom : " + self.cleaned_data["first_name"]
        new_line = "\n"

        message = new_line.join(
            (
                company_info,
                last_name_info,
                first_name_info,
                new_line,
                self.cleaned_data["content"]
            )
        )

        return message

    def send_email(self):
        """Get content and send email"""
        
        message = self.build_message_from_info

        send_mail(
            subject=self.cleaned_data["subject"],
            message=str(message),
            from_email=self.cleaned_data["from_email"],
            recipient_list=[VENTALIS_EMAIL],
            fail_silently=False,
        )
