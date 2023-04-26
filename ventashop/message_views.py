from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from ventashop.forms import MessageForm
from ventashop.models import Conversation, Message

class MessageListView(ListView, FormMixin):
    """Our message list view (e.g. display a conversation)."""

    model = Message
    # paginate_by = 5  # if pagination is desired
    template_name = 'ventashop/messages.html'
    context_object_name = 'message_list'

    form_class = MessageForm

    def get_queryset(self, *args, **kwargs):
        """Message list (aka one conversation) to be displayed."""

        user = self.request.user

        # n last messages to be displayed.
        if "last" in self.kwargs:   
            last = int(self.kwargs["last"])
            if user.role == "CUSTOMER":
                m_set = list(Message.objects.filter(conversation__customer_account=user.customeraccount))[-last:]
            else:
                m_set = list(Message.objects.filter(conversation__id=self.kwargs["pk"]))[-last:]
        
        # all messages to be displayed.
        else:                       
            if user.role == "CUSTOMER":
                m_set = Message.objects.filter(conversation__customer_account=user.customeraccount)
            else:
                m_set = Message.objects.filter(conversation__id=self.kwargs["pk"])

        return m_set

    def post(self, request, *args, **kwargs):
        """Handle new message POST request."""
        
        form = self.form_class(request.POST)
        conversation = get_object_or_404(Conversation, pk=self.kwargs["pk"])
        
        if form.is_valid():
            author = self.request.user.first_name
            content = form.cleaned_data["content"]
            conversation.add_message(author=author, content=content)

        return HttpResponseRedirect(reverse('ventashop:messages-last', args=(conversation.id, 5)))
        
    def get_context_data(self, **kwargs):
        """Related conversation and new message form to be displayed."""

        context = super().get_context_data(**kwargs)
        user = self.request.user

        # context["conversation"] = get_object_or_404(Conversation, pk=self.kwargs["pk"])
        if user.role == "CUSTOMER":
            context["conversation"] = get_object_or_404(Conversation, customer_account=user.customeraccount)
        else:
            # context["conversation"] = get_object_or_404(Conversation, customer_account__employee_reg=user.reg_number)
            context["conversation"] = get_object_or_404(Conversation, pk=self.kwargs["pk"])

        context["form"] = self.get_form(self.form_class)

        return context


class ConversationListView(ListView):
    """Our conversation list view."""

    model = Conversation
    # paginate_by = 5  # if pagination is desired
    template_name = 'ventashop/conversations.html'
    context_object_name = "conversation_list"

    def get_queryset(self):
        conversation_list = Conversation.objects.filter(
            customer_account__employee_reg=self.request.user.reg_number
        ).order_by("date_created")
        return conversation_list
