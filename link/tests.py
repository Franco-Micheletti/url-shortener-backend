"""
Product tests
"""
import json
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import UrlModel, UserUrls
from http.cookies import SimpleCookie
from login.models import CustomUser


class CreateShortUrl(APITestCase):
    """
    Test for create short url endpoint
    """

    def test_create_short_url(self):
        """
        Test for create short url endpoint
        Expected Result: status code 201, url created successfully
        """
        data = {
            "long_url": "https://www.youtube.com/watch?v=OoVf2w0WTY4&ab_channel=FranArgerich"
        }

        response = self.client.post(
            "/url/create_short_url", json.dumps(data, indent=4), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(UrlModel.objects.count(), 1)

    def test_error_create_short_url(self):
        """
        Test 2 for create short url endpoint
        Expected result: status code 400, error at creating the url.
        This is for testing requests with missing json data.
        """
        data = {

        }

        response = self.client.post(
            "/url/create_short_url", json.dumps(data, indent=4), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(UrlModel.objects.count(), 0)

    def test_error_create_short_url_2(self):
        """
        Test 3 for create short url endpoint
        Expected result: status code 400, error at creating the url.
        This test is for testing the validation of the long URL.
        """
        data = {
            "long_url": "https://com"
        }

        response = self.client.post(
            "/url/create_short_url", json.dumps(data, indent=4), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(UrlModel.objects.count(), 0)

    def test_error_create_short_url_3(self):
        """
        Test 4 for create short url endpoint
        Expected result: status code 400, error at creating the url.
        This test is for testing the validation of the long URL.
        """
        data = {
            "long_url": "this is not a normal url"
        }

        response = self.client.post(
            "/url/create_short_url", json.dumps(data, indent=4), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(UrlModel.objects.count(), 0)


class GetUrlObject(APITestCase):

    def test_get_url_object(self):
        """
        Test for fetching a url object with the provided short url argument.
        """
        data = {
            "long_url": "https://www.youtube.com/watch?v=OoVf2w0WTY4&ab_channel=FranArgerich"
        }

        response = self.client.post(
            "/url/create_short_url", json.dumps(data, indent=4), content_type='application/json')

        response = self.client.get(
            "/url/get_url/short_url="+response.json()["url"]["short_url"], content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)


class TestUserUrls(APITestCase):

    def test_get_user_urls(self):

        # Signup

        data = {
            "username": "franco",
            "firstname": "franco",
            "lastname": "micheletti",
            "email": "franco@hotmail.com",
            "birthday": "1990-06-15",
            "password": "!ert456Hdert-",
            "phone": "4343434344"
        }

        response = self.client.post(
            "/signup/", json.dumps(data, indent=4), content_type='application/json')
        self.assertEqual(CustomUser.objects.count(), 1)

        # Login

        data = {"username": "franco",
                "password": "!ert456Hdert-"}

        response = self.client.post(
            "/login/", json.dumps(data, indent=4), content_type='application/json')

        self.client.cookies = SimpleCookie(
            {'jwt_access': response.cookies.get("jwt_access")})

        # Create a URL for testing

        data = {
            "long_url": "https://www.youtube.com/watch?v=OoVf2w0WTY4&ab_channel=FranArgerich"
        }

        short_url_response = self.client.post(
            "/url/create_short_url", json.dumps(data, indent=4), content_type='application/json')
        self.assertEqual(short_url_response.status_code, HTTP_201_CREATED)
        self.assertEqual(UrlModel.objects.count(), 1)

        # Fetch the logged user's URLs

        user_urls_response = self.client.get(
            "/user_urls/all")

        self.assertEqual(user_urls_response.status_code, HTTP_200_OK)
        self.assertEqual(UserUrls.objects.count(), 1)
