from django.db import models

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class User(models.Model):
    LOGIN = models.ForeignKey(Login,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=300)
    housename = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)
    coins = models.CharField(max_length=100)

class Request(models.Model):
    wasterequest = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    USER = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    status = models.CharField(max_length=100)

class Request_sub(models.Model):
    REQUEST = models.ForeignKey(Request, on_delete=models.CASCADE, default=1)
    CATEGORY = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=100)

class Pickupdriver(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    lisenceno = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

class Schedule(models.Model):
    REQUEST_SUB = models.ForeignKey(Request_sub,on_delete=models.CASCADE,default=1)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    PICKUPDRIVER = models.ForeignKey(Pickupdriver, on_delete=models.CASCADE, default=1)

class Pickup(models.Model):
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    SCHEDULE = models.ForeignKey(Schedule, on_delete=models.CASCADE, default=1)
    Quantity = models.CharField(max_length=100)

class Coin(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    coin = models.CharField(max_length=100)

class Feedback(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    feedback = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

class Bank(models.Model):
    accountnumber = models.CharField(max_length=100)
    ifsccode = models.CharField(max_length=100)
    balance = models.FloatField()