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


class Order(models.Model):
    Order_Number = models.CharField(max_length=100)
    Order_Date = models.DateField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Phone_Number = models.BigIntegerField()
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pincode = models.BigIntegerField()
    Order_Status = models.CharField(max_length=100)

    class Meta:
        db_table = 'Order'


class Payment(models.Model):
    Customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Order_ID = models.ForeignKey(Order, on_delete=models.CASCADE)
    Payment_Status = models.CharField(max_length=100, default='Pending')
    Transaction_ID = models.CharField(max_length=200)
    Payment_Mode = models.CharField(max_length=100, default='PayU')

    class Meta:
        db_table = 'Payment'


class OrderDetail(models.Model):
    Order_Number = models.CharField(max_length=100)
    Customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Product_ID = models.ForeignKey(Book, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Total_Price = models.IntegerField()
    Payment_ID = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'OrderDetail'
