from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.mail import EmailMessage
from django.forms import ModelForm
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
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
class DepositAdmin(admin.ModelAdmin):
    list_display = ['txnId','amount','date','action', 'user']
    list_filter = ('date','user','action',)
    search_fields = ('amount','action',)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to send an email after a deposit is created.
        """
        # Save the deposit to the database
        super().save_model(request, obj, form, change)
        amount = obj.amount
        formatted_amount = f"{float(amount):,.2f}"

        # email context
        email_context ={
            "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            'user': obj.user,
            'amount': formatted_amount,
            'description': obj.action,
            'current_balance': obj.user.bal,
            'date': obj.date,
            'txnId': obj.txnId,
            'txnType': obj.txnType,
            'current_year': now().year,
            'status': obj.status
        }
        # Render the HTML template
        html_message = render_to_string("user_templates/email_templates/deposit_email.html", email_context)
        plain_message = strip_tags(html_message)  # Fallback for non-HTML clients

        # Send email to the user
        subject = 'Deposit Confirmation'
        recipient_email = obj.user.email

        email = EmailMessage(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        email.content_subtype = 'html'  # Indicate the email is HTML

        try:
            email.send()
        except Exception as e:
            self.message_user(request, f"Failed to send email: {e}", level="error")





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
    list_display = ('email', 'first_name', 'last_name', 'bal', 'account_number', 'bal', 'is_blocked', 'id')
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