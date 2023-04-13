
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


class ProductsMainViewTestCase(TestCase):
    """Test class for our main Products display view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.count = Product.objects.all().count()

        # 2 categories.
        cls.category1 = Category.objects.create(name="test1")
        cls.category2 = Category.objects.create(name="test2")
        
        # 2 products in same category1.
        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
            category=cls.category1
        )

        cls.product2 = Product.objects.create(
            name="product2", 
            description="description2",
            price=4242, 
            category=cls.category1
        )
    
    def test_all_products_display(self):
        """Test to check all products are displayed."""

        # Act.
        response = self.c.get("/products/")

        # Assert.
        self.assertContains(response, "product1")
        self.assertContains(response, "product2")

    def test_products_filtered_by_category(self):
        """Test to check products are displayed in their category."""
        
        # Act.
        url  = "/" + str(self.category1.name) + "/products/"
        response = self.c.get(url)

        # Assert.
        self.assertContains(response, "product1")
        self.assertContains(response, "product2")
        
    def test_products_filtered_by_category_empty_category(self):
        """Test to check no products are displayed in "empty" category."""

        # Act.
        url  = "/" + str(self.category2.name) + "/products/"
        response = self.c.get(url)

        # Assert.
        self.assertNotContains(response, "product1")
        self.assertNotContains(response, "product2")

# CHECK : https://docs.djangoproject.com/en/4.2/ref/utils/#django.utils.text.slugify