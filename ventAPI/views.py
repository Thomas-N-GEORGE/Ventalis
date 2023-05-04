from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, mixins
from rest_framework import permissions
from rest_framework.response import Response

from ventAPI.pemissions import IsEmployee

from ventashop.models import CustomerAccount, Order, Comment, Product, Message, Conversation, LineItem
from ventAPI.serializers import (
                                UserSerializer, 
                                CustomerAccountSerializer, 
                                OrderSerializer,
                                CommentSerializer,
                                ConversationSerializer,
                                MessageSerializer,
                                ProductSerializer,
                                LineItemSerializer,
                                WholeOrderSerializer,
                                )


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    -> Rather than write multiple views we're grouping together all the common behavior into classes called ViewSets.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CustomerAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customer accounts to be viewed or edited.
    """

    queryset = CustomerAccount.objects.all()
    serializer_class = CustomerAccountSerializer
    # permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee related orders to be viewed or edited.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

    
class UserRelatedOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee related orders to be viewed.
    """

    queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    serializer_class = WholeOrderSerializer
    # permission_classes = [permissions.IsAuthenticated, IsEmployee]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get user related order list."""
        
        user = self.request.user

        # Employee related order list.
        if user.role == "EMPLOYEE":
            queryset = Order.objects.all().filter(customer_account__employee_reg=user.reg_number)
        # Customer related order list.
        elif user.role == "CUSTOMER":
            queryset = Order.objects.all().filter(customer_account__customer=user)

        return queryset

    
class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows specific user conversations to be viewed or edited.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get a set of conversations if user is employee,
        or "THE" conversation if user is customer.
        """
        
        user = self.request.user
        queryset = Conversation.objects.filter(participants=user).order_by("date_modified")

        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    
class LineItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows line items to be viewed or edited.
    """

    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
    # permission_classes = [permissions.IsAuthenticated]
    

class WholeOrderViewListView(viewsets.ModelViewSet):
    """
    API endpoint that displays all details of anorder,
    with nested relationships.
    """

    queryset = Order.objects.all()
    serializer_class = WholeOrderSerializer
