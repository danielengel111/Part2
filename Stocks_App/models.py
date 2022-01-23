from django.db import models

# Create your models here.


class Transaction(models.Model):
    tDate = models.DateField(primary_key=True)
    ID = models.IntegerField()
    TQuantity = models.IntegerField()