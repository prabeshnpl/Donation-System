from django.db import models

# Create your models here.
class DonationAnalysis(models.Model):
    available_fund = models.IntegerField()
    

    