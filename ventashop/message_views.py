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
        """Conversation message list to be displayed."""

        if "last" in self.kwargs:   # n last messages
            last = int(self.kwargs["last"])
            m_set = list(Message.objects.filter(conversation__id=self.kwargs["pk"]))[-last:]
        
        else:                       # all messages
            m_set = Message.objects.filter(conversation__id=self.kwargs["pk"])

        return m_set

    def post(self, request, *args, **kwargs):
        """handle new message POST request."""
        
        form = self.form_class(request.POST)
        conversation = get_object_or_404(Conversation, pk=self.kwargs["pk"])
        
        if form.is_valid():
            author = "Tom"      # Hardcoded for now, user mechanism is not yet implemented.
            content = form.cleaned_data["content"]

            conversation.add_message(author=author, content=content)

        return HttpResponseRedirect(reverse('ventashop:messages-last', args=(conversation.id, 5)))
        
    def get_context_data(self, **kwargs):
        """Related conversation and new message form to be displayed."""

        context = super().get_context_data(**kwargs)
        context["conversation"] = get_object_or_404(Conversation, pk=self.kwargs["pk"])
        context["form"] = self.get_form(self.form_class)
        return context


class ConversationListView(ListView):
    """Our conversation list view."""

    model = Conversation
    # paginate_by = 5  # if pagination is desired
    template_name = 'ventashop/conversations.html'
    context_object_name = "conversation_list"
