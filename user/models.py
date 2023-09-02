from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.contrib.auth.models import Group, Permission
import random


class CustomUser(AbstractUser):
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    email_verification_code_expiry = models.DateTimeField(blank=True, null=True)
    #username = models.CharField(max_length=6, blank=False, null=False)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions"
    )
