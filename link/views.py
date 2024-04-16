from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.status import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from .functions.generate_random_url import generate_random_url
from .models import UrlModel
from .serializers import UrlModelSerializer, UrlModelGetSerializer
from django.middleware import csrf


class Url(APIView):

    def post(self, request):

        def CreateUrlObject(short_url, long_url):

            new_url = UrlModel.objects.create(
                short_url=short_url,
                long_url=long_url,
                clicks=0,
                created=datetime.now(),
                premium=False,
                last_access=datetime.now()
            )

            return new_url

        try:
            request_data = request.data
            long_url = request_data["long_url"]

            # Validate long url
            # Generate short url
            short_url = generate_random_url(6)
        except KeyError:
            return Response("JSON data is missing")

        try:
            # Check if the short url exists
            repeated_url = UrlModel.objects.get(
                short_url=short_url,
            )

            # The url is repeated generate a new short url
            short_url = generate_random_url(6)

            # Create a url object
            new_url = CreateUrlObject(short_url=short_url, long_url=long_url)

            response = {
                "message": "Url created successfully",
                "url": UrlModelSerializer(new_url).data
            }
            if new_url:
                return Response(response, status=HTTP_200_OK)

        except UrlModel.DoesNotExist:

            new_url = CreateUrlObject(
                short_url=short_url, long_url=long_url)

            response = {
                "message": "Url created successfully",
                "url": UrlModelSerializer(new_url).data
            }

            return Response(response, status=HTTP_200_OK)
        else:
            return Response("Error, url not created", HTTP_409_CONFLICT)

    def get(self, request, short_url):

        try:
            url_object = UrlModel.objects.get(short_url=short_url)
            return Response(UrlModelGetSerializer(url_object).data, status=HTTP_200_OK)
        except UrlModel.DoesNotExist:
            response = {
                "message": "The url does not exist",
                "code": 0}
            return Response(response, status=HTTP_404_NOT_FOUND)
