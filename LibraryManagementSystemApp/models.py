from django.db import models


# Create your models here.
class Customers(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    Phone = models.BigIntegerField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = "Customers"


class Books(models.Model):
    Name = models.CharField(max_length=200)
    Author = models.CharField(max_length=200)
    ISBN10 = models.BigIntegerField()
    Image = models.ImageField(upload_to="media")
    Price = models.IntegerField()
    Description = models.CharField(max_length=500)

    class Meta:
        db_table = "Books"
