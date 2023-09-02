from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("main", ComPostViewSet, basename="main")


urlpatterns = [
    path("", include(default_router.urls)),
]