from django.db import models
import re

# Create your models here.
class URL(models.Model):

    url = models.CharField(max_length=300)
    name = models.CharField(max_length=300)