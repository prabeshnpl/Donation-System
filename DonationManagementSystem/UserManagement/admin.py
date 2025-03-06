from django.contrib import admin
from .models import CustomUser,Donor,Beneficiary,DonationRequest,Donation

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','email','type')
    list_filter = ('phone_number','address')  
    
@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('receiver','title','status')
    list_filter = ('requested_date','requestedAmount')
    search_fields = ['status']
    ordering = ['-requested_date']

class DonationInline(admin.TabularInline):
    model = Donation
    extra = 1 

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    inlines = [DonationInline]

admin.site.register(Beneficiary)
