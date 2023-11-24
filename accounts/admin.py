from django.contrib import admin
from .models import Country, State, Profile, User, Beneficiary_Security_Details, Deposit, Transfer, Balance
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

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email']

