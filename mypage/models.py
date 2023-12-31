from django.db import models
from django.conf import settings

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    performance = models.CharField(max_length=50)
    performance_location = models.CharField(max_length=20)
    performance_date = models.DateTimeField()
    reservation_site = models.CharField(max_length=20)
    discount_method = models.CharField(max_length=10)
    price = models.PositiveIntegerField()
    ticket_memo = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ticket_number

class Memo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, default=0)
    location = models.CharField(max_length=20)
    date = models.DateField()
    content = models.TextField(max_length=200)