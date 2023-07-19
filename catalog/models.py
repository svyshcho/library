from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class LiteraryFormat(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(AbstractUser):
    pseudonym = models.CharField(max_length=63, null=True, blank=True)

    class Meta:
        ordering = ['username']
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    format = models.ForeignKey(
        LiteraryFormat,
        on_delete=models.CASCADE,
        related_name="books"
    )
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="books")

    def __str__(self):
        return f"{self.title} (price: {self.price}, format: {self.format})"

    class Meta:
        ordering = ["title"]