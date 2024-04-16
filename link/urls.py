from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("url/create_short_url", views.Url.as_view(), name="Create Short Url"),
    path("url/get_url/short_url=<short_url>",
         views.Url.as_view(), name="Get Short Url"),
]
