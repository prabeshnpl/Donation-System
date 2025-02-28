from django.contrib import admin
from .models import CustomUser,Donor,Beneficiary,DonationRequest,Donation
from .forms import RegisterForm


class CustomUserAdmin(admin.ModelAdmin):
    form = RegisterForm
    
    # def save_form(self, request, form, change):
    #     user_type = request.POST.get('usertype')  # Get the user_type from the form data
    #     return form.save(user_type=user_type)

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(DonationRequest)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Beneficiary)
