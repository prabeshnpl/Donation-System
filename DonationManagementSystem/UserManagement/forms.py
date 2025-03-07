from django import forms
from .models import CustomUser,DonationRequest,Donation

class RegisterForm(forms.ModelForm):
    
    re_enter_password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'register-confirm-password','type':'password'}),label='Confirm Password',required=True)

    class Meta:
        model = CustomUser
        fields = ['username','email','password','re_enter_password','type']
        labels={
            'username':'UserName',
            'email':'Email',
            'password':'Password',
            'type':'UserType',
        }
    
        widgets={
            'type':forms.RadioSelect(attrs={'class':'radio-container'})
            # 'username':forms.TextInput(attrs={'id':'register-name','type':'text'}),
            # 'email':forms.EmailInput(attrs={'id':'register-email','type':'email'}),
            # 'password':forms.PasswordInput(attrs={'id':'register-password','type':'password'}),
        }

    def save(self,**kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'login-user','type':'text'}),label='UserName')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'login-password','type':'password'}),label='Password')

class DonateForm(forms.ModelForm):

    """ Form for the donor to fill and donate """

    class Meta: 
        model = Donation
        fields = ['donatedAmount','description','donationMethod']
        labels={
            'donatedAmount':"Donation Amount (In Rs.)",
            'description':"Few Words on your Donation",
            'donationMethod':'Payment Method',
        }
        widgets={
            'donatedAmount':forms.TextInput(attrs={'type':"number"}),
            # 'description':forms.TextInput(attrs={'type':"text"}),
            # 'donationMethod':forms.ChoiceField()
        }

class RequestForm(forms.ModelForm):

    """ Request form for beneficiary to request donation """

    class Meta:
        model = DonationRequest
        fields = {'title','requestedAmount','description'}
        labels = {
            'title':'Reason for Request',
            'requestedAmount':'Fund Amount (In Rs.)',
            'description':'Describe the reason',
        }
        widgets={
            'title':forms.TextInput(attrs={'type':"text"}),
            'requestedAmount':forms.TextInput(attrs={'type':"number"}),
            'description':forms.TextInput(attrs={'type':"text"}),
        }

class UpdateProfileForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        # Fetch user from kwargs
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user:
            for fieldname in self.fields:
                if hasattr(user,fieldname): #Check if user has attribute as fieldname's value
                    self.fields[fieldname].initial = getattr(user,fieldname)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','address','phone_number','profile_picture']
        labels={
            'first_name':'First Name',
            'last_name':'Last Name',
            'email':'Email',
            'address':'Address',
            'phone_number':'Phone Number',
        }
        widgets={
            'first_name':forms.TextInput(attrs={'type':"text" ,'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'type':"text",'class':'form-control'}),
            'email':forms.EmailInput(attrs={'type':"email",'class':'form-control'}),
            'address':forms.TextInput(attrs={'type':"text",'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'type':"number",'class':'form-control'}),
        }
