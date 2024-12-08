from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.crypto import get_random_string
from django.contrib import messages
from .models import * 

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

@admin.register(VerificationCode)
class VerificationCodeEmail(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at', 'expires_at']

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'account_number', 'is_blocked')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_blocked', 'is_staff', 'is_superuser', 'is_active')

    # Organize fields in groups using fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bal')}),
        ('Account Status', {'fields': ('is_blocked', 'date_flagged')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    change_password_form = AdminPasswordChangeForm
    actions = ['block_users', 'unblock_users', 'reset_passwords']

    def block_users(self, request, queryset):
        updated_count = queryset.update(is_blocked=True)
        messages.success(request, f"{updated_count} user(s) have been blocked.")

    block_users.short_description = "Block selected users"
    
    def unblock_users(self, request, queryset):
        updated_count = queryset.update(is_blocked=False)
        messages.success(request, f"{updated_count} user(s) have been unblocked.")

    unblock_users.short_description = "Unblock selected users"

    def unblock_users(self, request, queryset):
        """
        Admin action to unblock selected users.
        """
        updated_count = queryset.update(is_blocked=False)
        messages.success(request, f"{updated_count} user(s) have been unblocked.")

    unblock_users.short_description = "Unblock selected users"

    def reset_passwords(self, request, queryset):
        """
        Admin action to reset passwords for selected users.
        """
        for user in queryset:
            new_password = get_random_string(8)  # Generate a random 8-character password
            user.set_password(new_password)
            user.save()
            user.email_user(
                subject="Your Password Has Been Reset",
                message=f"Your new password is: {new_password}\nPlease update it after logging in."
            )
        messages.success(request, "Passwords have been reset and emailed to the users.")

    reset_passwords.short_description = "Reset passwords for selected users"