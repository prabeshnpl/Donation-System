from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from UserManagement.models import DonationRequest,Beneficiary,Donor,Donation
from django.db.models import Sum,Count
from UserManagement.forms import DonateForm,RequestForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='user/login/')
def dashboard(request):
    donation_received = Donation.objects.filter(status='completed').aggregate(Sum('donatedAmount'),Count('donatedAmount'))
    donation_donated = DonationRequest.objects.filter(status='completed').aggregate(Sum('requestedAmount'),Count('requestedAmount'))
    all_donated_count = DonationRequest.objects.count()
    
    donation = Donation.objects.all().order_by('id')
    paginator = Paginator(donation,5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    
    return render(request,'dashboard.html',context={
        'available_fund':donation_received['donatedAmount__sum']-donation_donated['requestedAmount__sum'],

        'avg_donation_received': donation_received['donatedAmount__sum']/donation_received['donatedAmount__count'],
        'avg_donation_donated': donation_donated['requestedAmount__sum']/donation_donated['requestedAmount__count'],

        'received_count':donation_received['donatedAmount__count'],
        'pending_received_count': donation.count() - donation_received['donatedAmount__count'],

        'donation_donated_count':donation_donated['requestedAmount__count'],
        'pending_donation_donated_count':all_donated_count - donation_donated['requestedAmount__count'],

        'page_obj':page_obj, 
    })

 

@login_required(login_url='user/login/')
def my_donations(request):

    totaldonation = Donation.objects.filter(donor=request.user.donor,status='completed').aggregate(
        Sum('donatedAmount'),
        Count('donatedAmount'),
        )
    pending_donation = Donation.objects.filter(donor=request.user.donor,status='pending').aggregate(Sum('donatedAmount'),Count('donatedAmount'),)
    donation_stat = Donation.objects.filter(donor=request.user.donor).aggregate(Count('id'),Sum('donatedAmount'))

    donor = Donor.objects.get(user=request.user) 
    donations = Donation.objects.filter(donor=donor).prefetch_related('donor')

    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            donor = request.user.donor

            donation = form.save(commit=False)
            donation.donor = donor

            donation.save()
            messages.success(request,'Thank you for your donation.')
            return redirect('DashboardAnalytics:donated')
        else:
            messages.error(request,'Sorry form invalid!! Try again after some time.')
            return redirect('DashboardAnalytics:donated')


    return render(request,'my_donation.html',context={
        'total_donated':donation_stat['donatedAmount__sum'],
        'no_of_donations':donation_stat['id__count'],

        'completed_donation':totaldonation['donatedAmount__sum'],
        'pending_donation':pending_donation['donatedAmount__sum'],
        
        'completed_no':totaldonation['donatedAmount__count'],
        'pending_no':pending_donation['donatedAmount__count'],

        'donations':donations,
        'donation_form':DonateForm(),
    })

@login_required(login_url='user/login/')
def my_requests(request):

    total_req_amount = DonationRequest.objects.filter(receiver=request.user.beneficiary).aggregate(Sum('requestedAmount'),Count('requestedAmount'))

    active_request = DonationRequest.objects.filter(receiver=request.user.beneficiary,status='pending').aggregate(Sum('requestedAmount'),Count('requestedAmount'))

    request_received = DonationRequest.objects.filter(receiver=request.user.beneficiary,status='completed').aggregate(Sum('requestedAmount'),Count('requestedAmount'))

    receiver = Beneficiary.objects.get(user=request.user)
    donations = DonationRequest.objects.filter(receiver=receiver)

    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            receiver = request.user.beneficiary

            d_request = form.save(commit=False)
            d_request.receiver = receiver

            d_request.save()
            messages.success(request,'Thank you for your request. We will validate it shortly.')
            return redirect('DashboardAnalytics:requests')
        
        else:
            messages.error(request,'Sorry form invalid!! Try again after some time.')
            return redirect('DashboardAnalytics:requests')


    return render(request,'my_request.html',context={

                'no_of_req':total_req_amount['requestedAmount__count'],
                'total_req_amount':total_req_amount['requestedAmount__sum'],

                'no_of_active_req':active_request['requestedAmount__count'],
                'active_req_amount':active_request['requestedAmount__sum'],

                'no_of_req_received':request_received['requestedAmount__count'],
                'received_amount':request_received['requestedAmount__sum'],

                'donations':donations,
                'request_form': RequestForm(),
            })
