# from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
# from django.contrib.auth import get_user_model
from .models import User, State



class LoginForm(forms.Form):
    account_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Account Number",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))


class SignUpForm(forms.ModelForm):
    # firstname = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Firstname",                
    #             "class": "form-control"
    #         }
    #     ))
    # lastname = forms.CharField(
    # widget=forms.TextInput(
    #     attrs={
    #         "placeholder" : "lastname",                
    #         "class": "form-control"
    #     }
    # ))
    # middlename = forms.CharField(
    # widget=forms.TextInput(
    #     attrs={
    #         "placeholder" : "Middlename",                
    #         "class": "form-control"
    #     }
    # ))

    # nickname = forms.CharField(
    # widget=forms.TextInput(
    #     attrs={
    #         "placeholder" : "Nickname",                
    #         "class": "form-control"
    #     }
    # ))

    # email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "placeholder" : "Email",                
    #             "class": "form-control"
    #         }
    #     ))

    # phone_number = forms.IntegerField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Phone number",                
    #             "class": "form-control"
    #         }
    #     ))

    # dob = forms.DateField(
    #     widget=forms.DateInput(
    #         attrs={
    #             "placeholder" : "Date Of Birth",                
    #             "class": "form-control"
    #         }
    #     ))
        
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder" : "Password",                
    #             "class": "form-control"
    #         }
    #     ))
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder" : "Password check",                
    #             "class": "form-control"
    #         }
    #     ))


    class Meta: 
        model = User
        fields = ['email', 'phone_number','first_name','last_name', 
        'middle_name','nick_name', 'date_of_birth', 'title', 'gender',
        'zip_code','residential_address','account_type', 'city','ssn', 
        'State', 'country', 'Currency_type']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['State'].queryset = State.objects.none()

        if 'country' in self.data:
            try:
                print(self.data)
                country_id = int(self.data.get('country'))
                self.fields['State'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['State'].queryset = self.instance.country.city_set.order_by('name')
            

                


   

