
from decimal import Decimal

from django.test import Client, TestCase

# Create your tests here.

from ventashop.models import Category, Product


class StaticViewsTestCase(TestCase):
    """Test class for each of our static views."""

    def setUp(self):
        self.c = Client()

    def test_home(self):
        response = self.c.get("/")
        self.assertContains(response, "Produits de marketing")
    
    def test_about(self):
        response = self.c.get("/about/")
        self.assertContains(response, "Nous sommes une entreprise spécialisée")
    
    # def test_contact(self):
    #     response = self.c.get("/contact/")
    #     self.assertContains(response, "")
    
    # def test_login(self):
    #     response = self.c.get("/login/")
    #     self.assertContains(response, "")
    
    # def test_products(self):
    #     response = self.c.get("/products/")
    #     self.assertContains(response, "")
    
    # def test_category(self):
    #     response = self.c.get("/category/")
    #     self.assertContains(response, "")


class CategoryFormTestCase(TestCase):
    """Test class for our Category form."""

    def setUp(self) -> None:
        """Arrange."""

        self.c = Client()
        self.count = Category.objects.all().count()

    def test_category_created(self):
        """Test to check if new category is written to db."""

        # Act.
        self.c.post("/category_form/", {"name": "test"})

        # Assert
        self.assertEqual(self.count + 1, Category.objects.all().count())
    
    def test_category_unique(self):
        """Test to check if a category is unique in db."""

        # Act.
        self.c.post("/category_form/", {"name": "test"})
        self.c.post("/category_form/", {"name": "test"})

        # Assert
        self.assertEqual(self.count + 1, Category.objects.all().count())


class ProductFormTestCase(TestCase):
    """Test class for our Product form."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.count = Product.objects.all().count()
        cls.category = Category.objects.create(name="test")

    def create_a_product(self):
        """Simple method to create a product for test cases."""

        self.c.post(
            "/product_form/", 
            {
                "name": "test", 
                "description": "test description",
                "price": 42.42,
                "category": self.category.id,
            }
        )

    def test_product_created(self):
        """Test to check if new product is written to db."""

        # Act.
        self.create_a_product()

        # Assert
        self.assertEqual(self.count + 1, Product.objects.all().count())
    
    def test_product_unique(self):
        """Test to check if a product is unique in db."""

        # Act.
        self.create_a_product()
        self.create_a_product()

        # Assert
        self.assertEqual(self.count + 1, Product.objects.all().count())
