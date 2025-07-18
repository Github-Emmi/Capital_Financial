# from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
# from django.contrib.auth import get_user_model
from .models import User,Profile, State, Beneficiary_Security_Details
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


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

class XYZ_DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = '%d/%m/%Y'
        super().__init__(**kwargs)


class SignUpForm(forms.ModelForm):
    firstname = forms.CharField(
        required = True,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Firstname",                
                "class": "form-control",
                
            }
        ))
    lastname = forms.CharField(
    widget=forms.TextInput(
        attrs={
         "placeholder" : "lastname",                
            "class": "form-control",
            "required": True

        }
    ))
    

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                # "placeholder" : "Email",                
                "class": "form-control",
                "required": True
            }
        ))

    class Meta: 
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date_of_birth': XYZ_DateInput(format=["%Y-%m-%d"], ),
        }
        


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
                "placeholder" :  'Next Of Kin Residential Address'
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



class forgotPassForm(forms.Form):
    account_number = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder" : "Account Number",                
            "class": "form-control"
        }
    ))