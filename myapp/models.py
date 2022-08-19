from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
