from django.shortcuts import render

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "ventashop/home.html"


class AboutView(TemplateView):
    template_name = "ventashop/about.html"


class ContactView(TemplateView):
    template_name = "ventashop/contact.html"


class ProductView(TemplateView):
    template_name = "ventashop/products.html"


class LoginView(TemplateView):
    template_name = "ventashop/login.html"
