from django.db import models
from ..models import BaseModel


class Address(BaseModel):
    """
    Address model
    """
    street_address = models.CharField(
        max_length=200, blank=True, unique=False, null=True)
    extended_address = models.CharField(
        max_length=200, blank=True, unique=False, null=True)
    locality = models.CharField(max_length=20, unique=False, null=True)
    postal_code = models.CharField(max_length=20, unique=False, null=True)
    region = models.CharField(max_length=20, unique=False, null=True)

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.street_address


class Hotel(BaseModel):
    """
    Address model
    """
    name = models.CharField(max_length=200, blank=True,
                            unique=False, null=True)
    thumbnail_url = models.CharField(
        max_length=200, blank=True, unique=False, null=True)
    locality = models.CharField(max_length=20, unique=False, null=True)
    longitude = models.CharField(max_length=20, unique=False, null=True)
    latitude = models.CharField(max_length=20, unique=False, null=True)
    total_reviews = models.IntegerField(unique=False, null=True)
    star_rating = models.FloatField(unique=False, null=True)
    price = models.FloatField(unique=False, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                related_name="hotel_address", null=False)
    score = models.FloatField(max_length=10, null=True, blank=True)

    @property
    def rounded_rating(self):
        """
        Returns a rounded down rating
        """
        return (int(self.star_rating))

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.name