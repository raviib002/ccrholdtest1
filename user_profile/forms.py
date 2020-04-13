from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm)

from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, 
                                       UserChangeForm, PasswordResetForm, 
                                       SetPasswordForm, PasswordChangeForm)
from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from user_profile.models import AdditionalProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label=_("Email or Mobile Number"), max_length=254, widget=forms.TextInput(attrs={'class':'form-control lowercase','placeholder': 'Email or Mobile Number'}))
    password = forms.CharField(required=True, label=_("Password"), widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','placeholder': 'Password'}))
   
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
        return self.cleaned_data
    
"""For password reset form having email field"""
class PasswordResetFormUnique(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.TextInput(attrs={'class':'email form-control', 'placeholder':'Email', 'style':'text-transform:none;'}))
    def clean(self):
        cleaned_data = super(PasswordResetFormUnique, self).clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email address not recognized. There is no account linked to this email."))
        return cleaned_data


"""For password reset form having passwords field"""    
class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control ', 'id':'newpassword1', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'newpassword2', 'placeholder': 'Confirm New Password'})
    )
    old_password = forms.CharField(
        label=_("Current Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'oldpassword', 'placeholder': 'Current Password'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']
    
    
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class':'form-control resetpassword', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={'class':'form-control confirm-password-reset', 'placeholder': 'Confirm New Password'}))  
    
      
class RegistrationStep2(forms.Form):
#     first_name = forms.CharField(required=True, label='First Name',max_length='100', widget=forms.TextInput(attrs={'class':'form-control first_name'}))
#     last_name = forms.CharField(required=False,label='Last Name', widget=forms.TextInput(attrs={'class':'form-control last_name'}))
#     middle_name = forms.CharField(required=False,label='Middle Name',  widget=forms.TextInput(attrs={'class':'form-control middle_name'}))
    mobile_no = forms.CharField(required=True, max_length=10,label='Mobile Number', widget=forms.TextInput(attrs={'class':'form-control mobile_number'}))
#     email = forms.CharField(required=True, max_length=100, label='Email Id', widget=forms.TextInput(attrs={'class':'form-control email'}))
    pincode = forms.CharField(required=False, max_length=10, label='Pincode', widget=forms.TextInput(attrs={'class':'form-control pincode'}))
    address_line1 =  forms.CharField(required=False,label='Address 1', widget=forms.Textarea(attrs={'class':'form-control address1 ','rows':'2', 'cols':'5' }))
    address_line2 =  forms.CharField(required=False,label='Address 2', widget=forms.Textarea(attrs={'class':'form-control address2 ','rows':'2', 'cols':'5' }))

    class Meta:
        model = AdditionalProfile
        fields = ['mobile_no','pincode','address_line1','address_line2']

class RegistrationStep3(forms.Form):
    registration_no = forms.CharField(label='Registration No',max_length='100', widget=forms.TextInput(attrs={'class':'form-control registration_no'}))
    registration_certificate = forms.FileField( label='Registration Certificate',  widget=forms.FileInput(attrs={'accept': 'image/*'}))
    clinical_address1 =  forms.CharField(label='Clinical Address 1', widget=forms.Textarea(attrs={'class':'form-control clinical_address1 ','rows':'2', 'cols':'5' }))
    clinical_address2 =  forms.CharField(label='Clinical Address 2', widget=forms.Textarea(attrs={'class':'form-control clinical_address2 ','rows':'2', 'cols':'5' }))
    clinical_name = forms.CharField(label='Clinical Name',max_length='100', widget=forms.TextInput(attrs={'class':'form-control clinical_name'}))



        
        
        