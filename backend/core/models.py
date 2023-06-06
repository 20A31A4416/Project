from django.db import models

class pcloudAccount(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    auth = models.CharField(max_length=200, unique=True)
    lastUpdate = models.DateField(auto_now=True)
