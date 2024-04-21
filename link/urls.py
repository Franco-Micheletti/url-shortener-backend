from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("url/create_short_url", views.Url.as_view(), name="Create Short Url"),
    path("url/get_url/short_url=<short_url>",
         views.Url.as_view(), name="Get Short Url"),
    path("user_urls/all", views.UserUrl.as_view(), name="Get all user URLs"),
]
