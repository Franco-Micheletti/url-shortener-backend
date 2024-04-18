"""
Serializers
"""

from rest_framework import serializers
from .models import UrlModel, UserUrls


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


class UserUrlSerializer(serializers.ModelSerializer):
    """
    User's URLs Serializer
    """
    url = UrlModelGetSerializer()

    class Meta:
        """
        Metal Class
        """
        model = UserUrls
        fields = '__all__'
