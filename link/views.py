from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.status import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .functions.generate_random_url import generate_random_url
from .models import UrlModel, UserUrls
from .serializers import UrlModelSerializer, UrlModelGetSerializer, UserUrlSerializer
from django.middleware import csrf
import jwt
from django.conf import settings
from login.models import CustomUser
from django.utils import timezone
import validators


class Url(APIView):
    throttle_scope = 'link'

    def post(self, request):

        def CreateUrlObject(short_url, long_url):

            new_url = UrlModel.objects.create(
                short_url=short_url,
                long_url=str(long_url),
                clicks=0,
                created=timezone.now(),
                premium=False,
                last_access=timezone.now()
            )

            return new_url

        try:
            request_data = request.data
            long_url = request_data["long_url"]

            # Check if long url is valid

            validation = validators.url(long_url)

            if bool(validation) == False:
                return Response("URL is not valid", HTTP_400_BAD_REQUEST)

            # Generate short url
            short_url = generate_random_url(6)
        except KeyError:
            return Response("JSON data is missing", HTTP_400_BAD_REQUEST)

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
                return Response(response, status=HTTP_201_CREATED)

        except UrlModel.DoesNotExist:

            new_url = CreateUrlObject(
                short_url=short_url, long_url=long_url)

            # Update User Urls Model if user is logged in
            access_token = request.COOKIES.get("jwt_access")

            if access_token:
                user_data = jwt.decode(jwt=access_token,
                                       key=settings.SECRET_KEY,
                                       verify=True,
                                       algorithms=["HS256"])

                user = CustomUser.objects.get(id=user_data["user_id"])

                UserUrls.objects.create(
                    user=user,
                    url=new_url)

            response = {
                "message": "Url created successfully",
                "url": UrlModelSerializer(new_url).data
            }

            return Response(response, status=HTTP_201_CREATED)
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


class UserUrl(APIView):

    def get(self, request):

        access_token = request.COOKIES.get("jwt_access")

        if access_token:
            user_data = jwt.decode(jwt=access_token,
                                   key=settings.SECRET_KEY,
                                   verify=True,
                                   algorithms=["HS256"])

            user = CustomUser.objects.get(id=user_data["user_id"])

            # Get User Urls Model if user is logged in

            user_urls = UserUrls.objects.filter(
                user=user)

            user_urls_data = UserUrlSerializer(user_urls, many=True).data
            return Response(user_urls_data, status=HTTP_200_OK)
        else:
            return Response("Invalid Token", status=HTTP_401_UNAUTHORIZED)
