from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = "mypage"

urlpatterns = [
    path("mypage/ticket", TicketView.as_view(), name='ticket'),
]
