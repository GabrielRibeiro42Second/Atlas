from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_category_name_per_company",
            )
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
