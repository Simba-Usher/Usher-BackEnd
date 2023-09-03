from rest_framework import serializers
from .models import *

class TicketSerializer(serializers.Serializer):
    ticket_number = serializers.CharField()
    memo = serializers.CharField(required=False, allow_blank=True)