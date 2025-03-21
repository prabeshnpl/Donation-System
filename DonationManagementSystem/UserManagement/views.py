from django.shortcuts import render,redirect
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView,FormView
from .forms import LoginForm,RegisterForm, UpdateProfileForm
from .models import CustomUser,Donation,DonationRequest
# Create your views here.

class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('UserManagement:login')

    def form_valid(self,form):
        password = form.cleaned_data['password']
        re_enter_password = form.cleaned_data['re_enter_password']
        if password and re_enter_password and password == re_enter_password:
            user_type = form.cleaned_data['type']
            form.save(user_type=user_type)
            return super().form_valid(form=form)
        else:
            messages.error(self.request,'Password must be same')
            return redirect('UserManagement:register')
    
        
        
    def form_invalid(self, form):
        messages.error(self.request,'Invalid Form')
        return super().form_invalid(form)


class Login(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('UserManagement:dashboard')
    
    def form_valid(self,form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username = username,password=password)
        
        if user:
            login(self.request,user)
            return redirect('DashboardAnalytics:dashboard')
        else:
            messages.error(self.request,'Invalid Credentials') 
            return redirect('UserManagement:login')        
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid Form')
        return super().form_invalid(form)
 
    
def log_out(request):
    logout(request)
    return redirect('DashboardAnalytics:dashboard')


class Profile(LoginRequiredMixin,TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the user object to the form to load user 
        context['form'] = UpdateProfileForm(user=self.request.user)
        
        if self.request.user.type == 'beneficiary':
            # print('yes')
            pending = DonationRequest.objects.filter(receiver=self.request.user.beneficiary,status='pending').count()
            received = DonationRequest.objects.filter(receiver=self.request.user.beneficiary,status='completed').count()
            context['pending'] = pending
            context['received'] = received
        elif self.request.user.type == 'donor':
            pending = Donation.objects.filter(donor=self.request.user.donor,status='pending').count()
            total_donation = Donation.objects.filter(donor=self.request.user.donor).count()
            context['pending'] = pending
            context['total_donation'] = total_donation
        return context
    
    def post(self,request):

        if 'profile_picture' in request.FILES: 
            user = CustomUser.objects.get(pk=request.user.pk)
            user.profile_picture = request.FILES['profile_picture']
            user.save()
            return redirect('UserManagement:profile')
        
        else:
            form = UpdateProfileForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('UserManagement:profile')

            else:
                form = UpdateProfileForm(instance=request.user)
                return redirect('UserManagement:profile')

        
  
class ErrorView(TemplateView):
    template_name = 'error.html'



