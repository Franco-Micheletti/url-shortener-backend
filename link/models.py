"""
Link's models
"""
from django.db import models


class UrlModel(models.Model):
    """
    Model for URL table
    """

    short_url = models.CharField(
        max_length=300, null=True, blank=True, unique=True)
    long_url = models.CharField(max_length=300, null=True, blank=True)
    clicks = models.BigIntegerField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    premium = models.BooleanField(null=True, blank=True)
    last_access = models.DateTimeField(null=True, blank=True)
