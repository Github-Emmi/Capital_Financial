from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(cards)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','card_number','cvv']


@admin.register(DepositCheck)
class UserAdmin(admin.ModelAdmin):
    list_display = ['amount', 'front_check','user_id']


