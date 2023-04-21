"""Our model logic's test file."""

from decimal import Decimal

from django.test import TestCase

from ventashop.models import (Product, LineItem, 
                              Cart, Order, Comment, 
                              Conversation, Message, 
                              CustomerAccount)


class OrderTestCase(TestCase):
    """Test class for our Cart model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.order = Order.objects.create()

    def test_add_comment(self):
        """Check if comment is created."""

        # Arrange.
        com_count = Comment.objects.all().count()

        # Act.
        self.order.add_comment("test")
        order_comments = self.order.comment_set.all()

        # Assert.
        self.assertEqual(com_count + 1, Comment.objects.all().count())
        self.assertEqual(list(order_comments)[0].content, "test")


class CommentTestCase(TestCase):
    """Test class for our Comment model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.order = Order.objects.create()

    def test_message_ordering_in_queryset(self):
        """Check if ordering by descending datetime."""

        # Arrange.
        self.order.add_comment("test1")
        self.order.add_comment("test2")
        self.order.add_comment("test3")

        # Act.
        order_comments = self.order.comment_set.all()

        # Assert.
        self.assertTrue(
            order_comments[0].date_created > 
            order_comments[1].date_created > 
            order_comments[2].date_created
        )


class CartTestCase(TestCase):
    """Test class for our Cart model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
        )

        cls.product2 = Product.objects.create(
            name="product2", 
            description="description1",
            price=6789, 
        )

        cls.cart = Cart.objects.create()

    def test_initial_total_price_is_0(self):
        """Initial empty cart total is 0"""

        # Assert.
        self.assertEqual(self.cart.total_price, 0)
        
    def test_add_line_item(self):
        """
        Add a product to cart, 
        check if a relative line item is created,
        check the total price of cart.
        """

        # Arrange.
        li_set_count = LineItem.objects.filter(cart=self.cart).count()

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        li_set = self.cart.lineitem_set.all()

        # Assert.
        self.assertEqual(li_set_count + 1, LineItem.objects.filter(cart=self.cart).count())
        self.assertEqual(self.cart.total_price, self.product1.price * 1234)

    def test_add_line_item_quantity_less_than_1000(self):
        """
        Add a product to cart with quantity less than 1000, 
        check if no relative line item is created,
        check the total price of cart.
        """

        # Arrange.
        li_set_count = LineItem.objects.filter(cart=self.cart).count()

        # Act.
        self.cart.add_line_item(self.product1, 123)

        # Assert.
        self.assertEqual(li_set_count , LineItem.objects.filter(cart=self.cart).count())
        self.assertEqual(self.cart.total_price, 0)
    
    def test_add_same_product_twice_to_cart(self):
        """
        Add a product twice to cart (first with quantity >= 1000, secondly < 1000), 
        check if only a single relative line item is created,
        check the total price of cart.
        """

        # Arrange.
        li_set_count = LineItem.objects.filter(cart=self.cart).count()

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product1, 123)

        # Assert.
        self.assertEqual(li_set_count + 1, LineItem.objects.filter(cart=self.cart).count())
        self.assertEqual(self.cart.total_price, self.product1.price * (1234 + 123))

    def test_update_line_item(self):
        """
        Update a product quantity in cart, 
        check if only a single relative line item is created,
        check the total price of cart.
        """

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.update_line_item(self.product1, 5678)

        # Assert.
        self.assertEqual(self.cart.total_price, self.product1.price * 5678)
    
    def test_update_line_item_quantity_less_than_1000(self):
        """
        Update a product with quantity < 1000 in cart, 
        check if line item update is aborted.
        """

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.update_line_item(self.product1, 123)

        # Assert.
        self.assertEqual(self.cart.total_price, self.product1.price * 1234)

    def test_remove_line_item(self):
        """Check if line item is removed and cart total price updated."""

        # Arrange.
        self.cart.add_line_item(self.product1, 1234)

        li_set = LineItem.objects.filter(cart=self.cart)
        li_set_count = li_set.count()

        # Act.
        self.cart.remove_line_item(li_set[0])

        # Assert.
        self.assertEqual(self.cart.total_price, 0)
        self.assertEqual(LineItem.objects.filter(cart=self.cart).count(), li_set_count - 1)

    def test_empty_cart(self):
        """Check if line items are removed and cart total price reset to 0."""

        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product2, 5678)

        # Act.
        self.cart.empty_cart()

        # Assert.
        self.assertEqual(self.cart.total_price, 0)
        self.assertEqual(LineItem.objects.filter(cart=self.cart).count(), 0)

    def test_calculate_total_price(self):
        """Check for correct total price of cart."""

        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product2, 5678)

        # Act.
        self.cart.calculate_total_price()

        # Assert.
        self.assertEqual(self.cart.total_price, 4242 * 1234 + 6789 * 5678)

    def test_make_order_aborted_if_empty_cart(self):
        """
        Check if order is not created from  an "empty" cart, 
        """

        o_count = Order.objects.all().count()

        # Act.
        self.cart.make_order()

        # Assert.
        self.assertEqual(Order.objects.all().count(), o_count)

    def test_make_order_cart_emptied(self):
        """
        Check if order is created from our cart, 
        check is cart is "emptied", its total price reset to 0.
        """
        
        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        o_count = Order.objects.all().count()

        # Act.
        self.cart.make_order()

        # Assert.
        self.assertEqual(Order.objects.all().count(), o_count + 1)
        self.assertEqual(self.cart.lineitem_set.all().count(), 0)
        self.assertEqual(self.cart.total_price, 0)
    
    def test_make_order_check_order_is_correctly_populated(self):
        """
        Check created order from our cart has its fields correctly populated : 
        the line items should be passed to the order,
        the total price or the order sould be the same as was cart's.
        """
        
        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product2, 5678)
        cart_tp = self.cart.total_price
        li_list = list(self.cart.lineitem_set.all())

        # Act.
        self.cart.make_order()
        
        # Assert.
        o_set = Order.objects.all()
        order = o_set[o_set.count() - 1]

        self.assertListEqual(list(order.lineitem_set.all()), li_list)
        self.assertEqual(order.total_price, cart_tp)

    def test_make_order(self):
        """
        Check if order is created and cart is all reset, 
        with the line items "transfered" from cart to order.
        (Slightly redundant to previous tests). 
        """

        # Arrange.
        self.cart.add_line_item(self.product1, 1000)
        self.cart.add_line_item(self.product2, 1000)
        cart_total_price = self.cart.total_price
        line_item_set = self.cart.lineitem_set.all()

        # Act.
        order = self.cart.make_order()

        # Assert.
        self.assertEqual(self.cart.lineitem_set.all().count(), 0)
        self.assertEqual(self.cart.total_price, 0)
        self.assertEqual(order.total_price, cart_total_price)
        for li in range(0, line_item_set.count()):
            li_pk = li.pk
            self.assertIn(LineItem.objects.filter(pk=li_pk), order.lineitem_set.all())

    def test_make_order_assigns_new_order_to_customer_account(self):
        """Check if newly created order is assigned to customer account."""

        # Arrange.
        ca = CustomerAccount.objects.create()
        ca.create_cart()
        cart = ca.cart
        cart.add_line_item(self.product1, 1000)
        assigned_order_count = Order.objects.filter(customer_account = ca).count()

        # Act.
        cart.make_order()

        # Assert.
        self.assertEqual(assigned_order_count + 1, Order.objects.filter(customer_account = ca).count())



class LineItemTestCase(TestCase):
    """Test class for our Line Item model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
        )

    def test_line_item_quantity_ge_1000(self):
        """Test to check the quantity field is updated to 1000 if less."""

        # Act.
        li = LineItem.objects.create(product=self.product1, quantity=900)

        # Assert.
        self.assertEqual(li.quantity, 1000)

    def test_line_item_price_create(self):
        """Test to check the price field is populated correctly."""

        # Act.
        li = LineItem.objects.create(product=self.product1, quantity=1000)

        # Assert.
        self.assertEqual(self.product1.price * 1000, li.price)


class ConversationTestCase(TestCase):
    """Test class for our Convesation model logic."""

    def test_add_message(self):
        """Check if message is created when method is called."""

        # Arrange.
        conversation = Conversation.objects.create(subject="test")
        message_content = "This is a test."
        message_author = "Hi test."

        # Act.
        message_count = Message.objects.all().count()
        conversation.add_message(author=message_author, content=message_content)
        message = conversation.message_set.all()[0]

        # Assert.
        self.assertEqual(message_count + 1, Message.objects.all().count())
        self.assertEqual(message.author, message_author)
        self.assertEqual(message.content, message_content)


class CustomerAccountTestCase(TestCase):
    """Test class for our Convesation model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.cart_count = Cart.objects.all().count()
        cls.ca = CustomerAccount.objects.create()

    def test_create_cart(self):
        """Check if a related cart is created."""

        # Act.
        self.ca.create_cart()

        # Assert.
        self.assertEqual(self.cart_count + 1, Cart.objects.all().count())
        self.assertEqual(self.ca.cart.customer_account.pk, self.ca.pk)
    
    def test_create_cart_called_twice_does_not_create_second_cart(self):
        """Check if no second cart is created if method is called twice."""

        # Act.
        self.ca.create_cart()
        self.ca.create_cart()

        # Assert.
        self.assertEqual(self.cart_count + 1, Cart.objects.all().count())
        self.assertEqual(self.ca.cart.customer_account.pk, self.ca.pk)