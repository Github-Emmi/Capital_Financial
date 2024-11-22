from django.contrib import admin
from .models import * 
# Country, State, Profile, User, Beneficiary_Security_Details, Deposit, Transfer, Balance
# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ['name',]

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'country',]
    list_filter = ['name',]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birth','country','state',]
    list_filter = ['user',]

@admin.register(Deposit)
class UserAdmin(admin.ModelAdmin):
    list_display = ['txnId','amount','date','action', 'user_id']

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['txnId', 'formatted_amount', 'date', 'action', 'user_id']

    def formatted_amount(self, obj):
        try:
            # Convert the amount to a float and format with commas
            formatted = f"{float(obj.amount):,.2f}"
            return formatted
        except (ValueError, TypeError):
            # Handle cases where the amount is invalid or None
            return obj.amount  # Display as is if formatting fails

    formatted_amount.short_description = "Amount"  # Custom column name


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email','first_name','last_name','account_number','id','formatted_balance']

