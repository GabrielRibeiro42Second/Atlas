from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Company, Category, Product


class CategoryTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Barbearia do Matheus")
        self.category = Category.objects.create(
            name = "Cortes",
            company=self.company,
        )
    def test_get_category(self):
        response = self.client.get(f"/api/categories/{self.category.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Cortes")

    def test_update_category(self):
        response = self.client.put(
            f"/api/categories/{self.category.pk}",
            {"name": "Corte degradé", "company": self.company.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Corte degradé")

    def test_create_category(self):
        response = self.client.post(
            "/api/categories",
            {"name": "Lavagem", "company": self.company.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Lavagem")

    def test_delete_category(self):
        response = self.client.delete(
            f"/api/categories/{self.category.pk}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

    def test_delete_category_not_found(self):
        response = self.client.delete(
            "/api/categories/99999"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_category_with_product(self):
        Product.objects.create(name="Corte navalha", category=self.category)
        response = self.client.delete(
            f"/api/categories/{self.category.pk}",
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())

    def test_lists_category(self):
        Category.objects.create(name="Barba", company=self.company)
        response = self.client.get("/api/categories")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_category_duplicate_name(self):
        response = self.client.post(
            "/api/categories",
            {"name": "Cortes", "company": self.company.pk},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name = "Barba na navalha")
        self.category = Category.objects.create(name = "Cortes", company = self.company)
        self.product = Product.objects.create(name = "Corte Maquina", category = self.category)

    def test_create_product(self):
        response = self.client.post(
            "/api/products",
            {"name": "Corte maquina", "category": self.category.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Corte maquina")

    def test_list_product(self):
        Product.objects.create(name="Corte tesoura", category=self.category)
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item["name"] for item in response.data]
        self.assertCountEqual(names, ["Corte Maquina", "Corte tesoura"])

    def test_get_product(self):
        response = self.client.get(
            f"/api/products/{self.product.pk}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Corte Maquina")

    def test_update_product(self):
        response = self.client.put(
            f"/api/products/{self.product.pk}",
            {"name": "Corte Maquina Zero", "category": self.category.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Corte Maquina Zero")

    def test_delete_product(self):
        response = self.client.delete(
            f"/api/products/{self.product.pk}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_delete_product_not_found(self):
        response = self.client.delete(
            f"/api/products/99999"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CompanyTest(APITestCase):
    def test_create_company(self):
        response = self.client.post(
            "/api/companies",
            {"name": "Mercado do Bairro"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Mercado do Bairro")
