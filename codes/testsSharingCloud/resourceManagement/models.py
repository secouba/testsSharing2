from django.db import models

# Create your models here.

class Users(models.Model):
    lastName = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    
class Resource(models.Model):
    resourceType = models.CharField(max_length=200)
    localisation = models.CharField(max_length=200)
    capacity = models.CharField(max_length=200)
    
class Booking(models.Model):
    titleB = models.CharField(max_length=500)
    startDate = models.DateField(null=False)
    endDate = models.DateField(null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    
    

    
