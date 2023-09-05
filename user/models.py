from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.contrib.auth.models import Group, Permission
import random

class CustomUser(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname'] 

    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    email_verification_code_expiry = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(unique=True) 
    nickname = models.CharField(max_length=6, unique=True)
    GRADE_CHOICES = [
        ('리허설', '리허설'),
        ('오버츄어', '오버츄어'),
        ('앙상블', '앙상블'),
        ('피날레', '피날레')
    ]
    grade = models.CharField(
        max_length=6, 
        choices=GRADE_CHOICES,
        default='리허설')


    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions"
    )
