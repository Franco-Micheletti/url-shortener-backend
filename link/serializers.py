"""
Serializers
"""

from rest_framework import serializers
from .models import UrlModel


class LinkSerializer(serializers.ModelSerializer):
    """
    Link Serializer
    """
    class Meta:
        """
        Meta class
        """
        model = UrlModel
        fields = ('short_url',
                  )
