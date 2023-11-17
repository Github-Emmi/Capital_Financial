# from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
# from django.contrib.auth import get_user_model
from .models import User,Profile, State, Beneficiary_Security_Details
from django.db import transaction



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
    firstname = forms.CharField(
        required = True,
        widget=forms.TextInput(
            attrs={
<<<<<<< HEAD
                # "placeholder" : "Firstname",                
=======
                "placeholder" : "Firstname",                
>>>>>>> origin/master
                "class": "form-control",

            }
        ))
    lastname = forms.CharField(
    widget=forms.TextInput(
        attrs={
<<<<<<< HEAD
            # "placeholder" : "lastname",                
=======
            "placeholder" : "lastname",                
>>>>>>> origin/master
            "class": "form-control",
            "required": True

        }
    ))
<<<<<<< HEAD
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
=======
   
>>>>>>> origin/master

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
<<<<<<< HEAD
                # "placeholder" : "Email",                
=======
                "placeholder" : "Email",                
>>>>>>> origin/master
                "class": "form-control",
                "required": True
            }
        ))

<<<<<<< HEAD
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
=======
    
>>>>>>> origin/master

# 'email','first_name','last_name'
    class Meta: 
        model = Profile
        fields = '__all__'
        exclude = ['user']
        # [
        # 'middle_name', 'phone_number','nick_name', 'date_of_birth', 'title', 'gender',
        # 'zip_code','residential_address','account_type', 'city','ssn', 
        # 'State', 'country', 'Currency_type']
        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['residential_address'].widget.attrs.update({
                'class': (
                    'form-control'
                ),
                "placeholder" :  'Residential Address',
                "required": True
            })
        # self.fields['date_of_birth'].widget.attrs.update({
        #     'DateInput'
        # })
        # forms.SelectDateWidget
<<<<<<< HEAD
=======
        self.fields['phone_number'].widget.attrs.update({
            "placeholder" :  'Phone Number',
            "required": True
            })

        self.fields['city'].widget.attrs.update({
                "placeholder" :  'city',
                "required": True
            })
        self.fields['ssn'].widget.attrs.update({
                
                "placeholder" :  'SSN',
                "required": True
            })
        self.fields['nick_name'].widget.attrs.update({
                
                "placeholder" :  'Nick Name',
                "required": True
            })
        self.fields['middle_name'].widget.attrs.update({
                "placeholder" :  'Middle Name',
                "required": True
            })
        self.fields['date_of_birth'].widget.attrs.update({
                "placeholder" :  'YYYY-MM-DD',
                "required": True
            })
        self.fields['zip_code'].widget.attrs.update({
                "placeholder" :  'Zip code',
                "required": True
            })
>>>>>>> origin/master
    

        self.fields['state'].queryset = State.objects.none()

        if 'country' in self.data:
            try:
                # print(self.data)
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.city_set.order_by('name')
          

    


class EmploymentInfo(forms.ModelForm):        
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Account Password",                
                "class": "form-control"
            }
        ))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Account Password",                
                "class": "form-control"
            }
        ))

    PIN = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "placeholder" : "Account PIN",                
                "class": "form-control"
            }
        ))

    
    class Meta:
        model = Beneficiary_Security_Details
        fields= '__all__'
        exclude = ['user']

        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nok_address'].widget.attrs.update({
                'class': (
                    'form-control'
                ),
<<<<<<< HEAD
                "placeholder" :  'Next Of Kin Residential Address'
=======
                "placeholder" :  'Next Of Kin Residential Address',
                "required": True
            })
        self.fields['beneficiary_legal_name'].widget.attrs.update({
                
                "placeholder" :  'Beneficiary\'s Legal Name',
                "required": True
>>>>>>> origin/master
            })

    

class ImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['avatar']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['avatar'].widget.attrs.update({
                'id': (
                    'filetag'
                ),
            })