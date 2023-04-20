"""
The file containing all our forms
Unused at this time
"""

from django import forms
from django.forms import ModelForm
from ventashop.models import Category


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
    """Our new message form"""

    content = forms.CharField(label="Nouveau message", max_length=5000)
