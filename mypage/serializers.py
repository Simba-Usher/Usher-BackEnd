from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    ticket_number = serializers.CharField()
