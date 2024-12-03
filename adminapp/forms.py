from django import forms
from .models import *
from .widgets import MonthYearWidget
from django.contrib.auth import get_user_model
from django.forms import ChoiceField



class XYZ_DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = '%d/%m/%Y'
        super().__init__(**kwargs)


class Check_DepositForm(forms.ModelForm):

    class Meta:
        model = DepositCheck
        fields = '__all__'
        exclude = ['user']
        

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['front_check'].widget.attrs.update({
                'id': (
                    'filetag'
                ),
                'class': (
                    'custom-file-input'
                ),
            })

        self.fields['back_check'].widget.attrs.update({
            'id': (
                'filetag_back'
            ),
            'class': (
                'custom-file-input'
            ),
        })
        self.fields['amount'].widget.attrs.update({
            'class': (
                'form-control form-control-lg form-control-number'
            ),
            "required": True
        })


class VerificationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        label='Enter Verification Code',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class XYZ_MonthInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%m"
        # kwargs["format"] = '%d/%m/%Y'
        super().__init__(**kwargs)

class XYZ_YearInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y"
        # kwargs["format"] = '%d/%m/%Y'
        super().__init__(**kwargs)

# class XYZ_DateInput(forms.DateInput):
#     input_type = "date"
#     def __init__(self, **kwargs):
#         kwargs["format"] = "%Y-%m-%d"
#         # kwargs["format"] = '%d/%m/%Y'
#         super().__init__(**kwargs)

class addCardForm(forms.ModelForm):

    # expiry_month = forms.DateField(
    #     widget=forms.SelectDateWidget(
    #         attrs={
    #         #     "placeholder" : "Account Number",                
    #             "class": "form-select form-control-sm"
    #         }
    #     ))
    # date = forms.DateField(
    #     required=False,
    #     widget=MonthYearWidget(years=xrange(2004,2010))
    # )

    class Meta:
        model = cards
        fields = '__all__'
        exclude = ['user', 'count']
        widgets = {
            'expiry_month': MonthYearWidget(),
            # 'expiry_month': XYZ_MonthInput(format=["%m"], ),
            # 'expiry_year': XYZ_YearInput(format=["%Y"], ),

        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['name'].widget.attrs.update({
                'class': (
                    'form-control form-control-xl form-control-outlined'
                    
                ),
                })
            
            self.fields['card_number'].widget.attrs.update({
                'class': (
                    'form-control form-control-xl form-control-outlined'
                        
                    ),
                })



            self.fields['cvv'].widget.attrs.update({
                'class': (
                    'form-control form-control-xl form-control-outlined'
                        
                    ),
                })

            self.fields['expiry_month'].widget.attrs.update({
            'class': (
            
                'form-control form-control-xl form-control-outlined'
                    
                ),
            })

            self.fields['expiry_year'].widget.attrs.update({
            'class': (
                'mr-3',
                'form-control form-control-xl form-control-outlined'
                    
                ),
            })






class setNewPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "New Password",                
                "class": "form-control form-control-md form-control-number",
                "required": "True"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm New Password",                
                "class": "form-control form-control-md form-control-number",
                "required": "True"

            }
        ))


class addNewBillerForm(forms.ModelForm):
    class Meta:
        model = paybillUser
        fields = '__all__'
        exclude = ['user']


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['name'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

            self.fields['payment_method'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })
            
            self.fields['account_number'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

            self.fields['address1'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

            self.fields['address2'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                ),
                })

            self.fields['state'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

            self.fields['zip_code'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

            self.fields['city'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

            self.fields['nickname'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })


class payBillByUser(forms.ModelForm):
    


    class Meta:
        model = paybills
        fields = ['amount', 'delivery_date','paid_to','action']
        widgets = {
            'delivery_date': XYZ_DateInput(format=["%Y-%m-%d"], ),
        }

    def __init__(self, user, *args, **kwargs):
        

        super(payBillByUser, self).__init__(*args, **kwargs)

        self.fields['paid_to'].queryset=paybillUser.objects.filter(user_id=user.id)

        self.fields['paid_to'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })

        self.fields['delivery_date'].widget.attrs.update({
                'class': (
                    'form-control form-control-outlined'
                    
                ),
                })


        self.fields['amount'].widget.attrs.update({
                'class': (
                    'form-control form-control-lg form-control-outlined'
                    
                ),
                })

        self.fields['action'].widget.attrs.update({
                'class': (
                    'form-control form-control-lg forr'
                    
                ),
                })
