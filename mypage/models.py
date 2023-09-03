from django.db import models
from django.conf import settings

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    performance_location = models.CharField(max_length=20)
    performance_date = models.DateTimeField()
    reservation_site = models.CharField(max_length=20)
    discount_method = models.CharField(max_length=10)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.ticket_number