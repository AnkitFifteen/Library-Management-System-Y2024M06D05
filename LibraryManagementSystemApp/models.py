from django.db import models


# Create your models here.
class Customer(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    Phone = models.BigIntegerField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = "Customer"


class Book(models.Model):
    Name = models.CharField(max_length=200)
    Author = models.CharField(max_length=200)
    ISBN10 = models.BigIntegerField()
    Image = models.ImageField(upload_to="media")
    Price = models.IntegerField()
    Description = models.CharField(max_length=9000)

    class Meta:
        db_table = "Book"


class Cart(models.Model):
    CID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    PID = models.ForeignKey(Book, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Total_Amount = models.FloatField()

    class Meta:
        db_table = 'Cart'
