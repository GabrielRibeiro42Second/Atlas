from django.db import transaction
from .models import Company, Product

@transaction.atomic
def delete_company(company):
    Product.objects.filter(category__company=company).delete()
    company.delete()
