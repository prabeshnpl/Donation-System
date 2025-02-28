from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,DonationRequest,Beneficiary,Donor

@receiver(post_save,sender=CustomUser)
def create_BeneficiaryOrDonor(sender,instance,created,**kwargs):
    if created:
        if instance.type == 'donor':
            Donor.objects.create(user=instance)
        else:
            Beneficiary.objects.create(user=instance)