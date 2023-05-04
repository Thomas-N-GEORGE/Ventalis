"""Our model serializer module."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from ventashop.models import (
                            CustomerAccount, 
                            Order, 
                            Conversation, 
                            Message, 
                            LineItem, 
                            Comment, 
                            Product,
                            )

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    conversation_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    message_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    customer_account_set = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ["id", 'email', 'first_name', 'last_name', 'reg_number', 'role', "conversation_set", "message_set", "customer_account_set"]
        read_only_fields = ["id", 'email', 'first_name', 'last_name', 'reg_number', 'role', "conversation_set", "message_set", "customer_account_set"]

class CustomerAccountSerializer(serializers.ModelSerializer):
    """CustomerAccount model serializer."""
    
    customer = serializers.ReadOnlyField(source="customer.email")
    order_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomerAccount
        fields = ["customer", "employee_reg", "order_set"]
        read_only_fields = ["employee_reg", "order_set"]


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    order = serializers.ReadOnlyField(source="order.pk")
    order_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ["content", "date_created", "order", "order_id"]


class OrderSerializer(serializers.ModelSerializer):
    """Order model serializer."""
    
    customer_account = serializers.ReadOnlyField(source="customer_account.pk")
    lineitem_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "vat_amount", "incl_vat_price", "date_created", "ref_number", "slug", "customer_account", "lineitem_set", "comment_set"]
        read_only_fields = ["id", "total_price", "vat_amount", "incl_vat_price", "date_created", "ref_number", "slug", "customer_account", "lineitem_set", "comment_set"]


class MessageSerializer(serializers.ModelSerializer):
    """Message model serializer."""

    author = serializers.ReadOnlyField(source="author.email")
    conversation = serializers.ReadOnlyField(source="conversation.id")
    conversation_id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ["id", "author", "date_created", "content", "is_read", "conversation", "conversation_id"]
        read_only_fields = ["date_created"]


class ConversationSerializer(serializers.ModelSerializer):
    """Conversation model serializer."""

    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # message_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    message_set = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        # fields = ["id", "subject", "date_created", "date_modified", "participants", "message_set"]
        fields = ["id", "subject", "date_created", "date_modified", "participants", "message_set"]
        read_only_fields = ["subject", "date_created"]


class ProductSerializer(serializers.ModelSerializer):
    """Product model serializer."""

    class Meta:
        model = Product
        fields = ["name", "price"]
        read_only_fields=["name", "price"]


class LineItemSerializer(serializers.ModelSerializer):
    """LineItem model serializer."""

    product = serializers.ReadOnlyField(source="product.name")
    order = serializers.ReadOnlyField(source="order.id")

    class Meta:
        model = LineItem
        fields = ['product', 'quantity', 'price', 'order']
        read_only_fields=["quantity", "price"]


class WholeOrderSerializer(OrderSerializer):
    """Order model serializer with all details."""

    lineitem_set = LineItemSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "vat_amount", "incl_vat_price", "date_created", "ref_number", "slug", "customer_account", "lineitem_set", "comment_set"]
        read_only_fields = ["id", "total_price", "vat_amount", "incl_vat_price", "date_created", "ref_number", "slug", "customer_account", "lineitem_set", "comment_set"]
