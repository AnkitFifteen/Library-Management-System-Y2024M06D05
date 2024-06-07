from django.db import models

# Create your models here.
class Customer(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    Phone = models.BigIntegerField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = "Customer"