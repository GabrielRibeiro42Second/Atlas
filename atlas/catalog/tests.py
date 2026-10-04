from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Company, Category


class CategoryRetrieveTests(APITestCase):
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
