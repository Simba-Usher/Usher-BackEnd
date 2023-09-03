from django.db import models
from django.conf import settings

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    performance = models.CharField(max_length=50)
    performance_location = models.CharField(max_length=20)
    performance_date = models.DateTimeField()
    reservation_site = models.CharField(max_length=20)
    discount_method = models.CharField(max_length=10)
    price = models.PositiveIntegerField()
    memo = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.ticket_number