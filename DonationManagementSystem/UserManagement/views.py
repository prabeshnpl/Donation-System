from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView,FormView
from .forms import LoginForm,RegisterForm
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
  
class ErrorView(TemplateView):
    template_name = 'error.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['error'] = 


