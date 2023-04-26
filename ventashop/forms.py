"""
The file containing all our forms
Unused at this time
"""

from django import forms
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.forms import ModelForm

from ventashop.models import Category, User, Cart, CustomerAccount
from ventashop.utils import unique_reg_number_generator
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


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class UserForm(forms.ModelForm):

    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    company = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'company']

    def create_user(self, role):
        """
        Create a user with a role,
        and complete processing according to role.
        """

        user, created = User.objects.get_or_create(
            email=self.cleaned_data["email"],
            password=make_password(self.cleaned_data["password"]),
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            # company=self.cleaned_data["company"],
            role=role,
        )

        if created:
            if role == "EMPLOYEE":      
                # Creation of a unique registration number
                user.reg_number = unique_reg_number_generator(user)
                user.company = "Ventalis"
                user.save()
            
            else:   
                # Case role == CUSTOMER
                # Create customer account, assign its employee reg number, related cart, and a related conversation.
                customer_account = CustomerAccount.objects.create(customer=user)
                customer_account.set_cart()
                customer_account.set_conversation(subject="Échanges avec mon conseiller")
                customer_account.set_employee_reg_number()
        
        return user
