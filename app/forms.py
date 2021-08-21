from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm
# from django.forms import fields, models, widgets
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import Customer

class CustomerRegister(UserCreationForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                'class': 'form-control',
                                                                }))

    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                'class': 'form-control',
                                                                }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                'class': 'form-control',
                                                                }))                                                                                                                        
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        label = {
            'email':'Emal',
            'password1':'Password',
            'password2':'Confirm Password'

        }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'})
        }

class UserLogin(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs={'placeholder':'username',
    'class':'form-control','autofocus':True}))
    password = forms.CharField(strip=False, widget = forms.PasswordInput(attrs={'placeholder':'password',
    'class':'form-control','autocomplete':'current-password'}))    

class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','autofocus': True , 'class':'form-control'}))

    new_password1 = forms.CharField(label="New Password",strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
    help_text=password_validation.password_validators_help_text_html() )

    new_password2 = forms.CharField(label="Confirm Password",strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))


class UserProfile(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','states','pincode']
        widgets = {

            'name':forms.TimeInput(attrs={'class':'form-control'}),
            'locality':forms.TimeInput(attrs={'class':'form-control'}),
            'city':forms.TimeInput(attrs={'class':'form-control'}),
            'states':forms.Select(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'})
            
        }