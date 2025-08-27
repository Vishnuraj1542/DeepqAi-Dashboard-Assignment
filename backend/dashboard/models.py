from django.db import models
from django.contrib.auth.models import User


class Indicator(models.Model):
    country = models.CharField(max_length=100, default="India")
    indicator = models.CharField(max_length=200)
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.indicator
    