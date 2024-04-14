from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("url/create_short_url", views.Url.as_view()),
]
