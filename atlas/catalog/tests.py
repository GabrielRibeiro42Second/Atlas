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
    def test_retrieve_category(self):
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
            f"/api/categories/{self.company.pk}",
            {"name": "Lavagem", "company": self.company.pk},
            format="json",
        )
    def test_create_product(self):
        response = self.client.post(
            "api/products",
            {"name": "Corte maquina", "category": self.category.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Corte maquina")
