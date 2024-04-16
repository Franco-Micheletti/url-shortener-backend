"""
Serializers
"""

from rest_framework import serializers
from .models import UrlModel


class UrlModelSerializer(serializers.ModelSerializer):
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


class UrlModelGetSerializer(serializers.ModelSerializer):
    """
    Link Serializer
    """
    class Meta:
        """
        Meta class
        """
        model = UrlModel
        fields = '__all__'
