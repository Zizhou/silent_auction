from django.db import models
from django import forms
from django.contrib.auth.models import User

import datetime, uuid

# Create your models here.
# that I will

class Auction(models.Model):
    item_name = models.CharField(max_length = 200, unique = True)
    uuid = models.CharField(max_length = 200, unique = True, blank = True, null = True)

