from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """ User class for authentication and validity """
    USER_TYPE = [
        ('donor','Donor'),
        ('beneficiary','Beneficiary'),
    ]
    username = models.CharField(max_length=64,blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    type = models.CharField(max_length=20,choices=USER_TYPE,default='donor')
     

    def __str__(self):
        return self.username
    
class Donor(models.Model):

    """ Donor class for donor related data """

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='donor')
    address = models.CharField(max_length=128,blank=True,null=True)
    # phone_number = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f'{self.user}'
    
class Beneficiary(models.Model):

    """ Beneficiary class for beneficiary related data """

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='beneficiary')
    totalReceived = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=128,blank=True,null=True)
    # phone_number = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f'{self.user}'
    
class DonationRequest(models.Model):

    """ Donations requested by beneficiary """

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed')
    ]

    receiver = models.ForeignKey(Beneficiary,on_delete=models.CASCADE,related_name='donation_request')
    title = models.CharField(max_length=64)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    requestedAmount = models.IntegerField()
    description = models.TextField()
    requested_date = models.DateField(auto_now_add=True)
 

    def __str__(self):
        return self.title

class Donation(models.Model):

    """ Donations donated by donors """

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed')
    ]
    DONATION_METHOD = [
        ('esewa','Esewa'),
        ('khalti','Khalti'),
        ('imepay','ImePay'),
    ]
    donor = models.ForeignKey(Donor,on_delete=models.SET_NULL,related_name='donation',null=True)
    donatedAmount = models.IntegerField()
    description = models.TextField()
    donationMethod = models.CharField(max_length=20,choices=DONATION_METHOD)
    donated_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f'{self.donor.user} : ({self.pk}) - Rs.{self.donatedAmount}'