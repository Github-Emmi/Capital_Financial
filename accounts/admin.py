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
    list_display = [
        "name",
    ]
    list_filter = [
        "name",
    ]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "country",
    ]
    list_filter = [
        "name",
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "date_of_birth",
        "country",
        "state",
    ]
    list_filter = [
        "user",
    ]


@admin.register(AccountDetails)
class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'routing_number', 'recipient_name')
    search_fields = ('bank_name', 'account_number', 'recipient_name')


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ["txnId", "amount", "date", "action", "user"]
    list_filter = (
        "date",
        "user",
        "action",
    )
    search_fields = (
        "amount",
        "action",
    )

    def save_model(self, request, obj, form, change):
        """
        Override save_model to send an email after a deposit is created.
        """
        # Save the deposit to the database
        super().save_model(request, obj, form, change)
        amount = obj.amount
        formatted_amount = f"{float(amount):,.2f}"

        current_balance = obj.user.bal
        formatted_balance = f"{float(current_balance):,.2f}"

        # email context
        subject = "Deposit Confirmation"
        email_context = {
            "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            "user": obj.user,
            "amount": formatted_amount,
            "description": obj.action,
            "current_balance": formatted_balance,
            "date": obj.date,
            "txnId": obj.txnId,
            "txnType": obj.txnType,
            "current_year": now().year,
            "status": obj.status,
        }
        # Render the HTML template
        html_message = render_to_string(
            "user_templates/email_templates/deposit_email.html", email_context
        )
        recipient_email = obj.user.email

        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        email.content_subtype = "html"  # Indicate the email is HTML

        try:
            email.send()
        except Exception as e:
            self.message_user(request, f"Failed to send email: {e}", level="error")


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ["txnId", "formatted_amount", "date", "action", "user_id"]

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
    list_display = ["user", "code", "created_at", "expires_at"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "formatted_balance",
        "account_number",
        "is_blocked",
        "is_marked",
        "id",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    list_filter = ("is_blocked", "is_marked", "is_staff", "is_superuser", "is_active")

    # Organize fields in groups using fieldsets
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "bal", "avatar", "account_number")}),
        ("Account Status", {"fields": ("is_marked", "is_blocked", "date_flagged")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    change_password_form = AdminPasswordChangeForm
    actions = ["mark_users", "unmark_users", "block_users", "unblock_users", "reset_passwords"]

    ##### Mark a user for a pending transaction
    def mark_users(self, request, queryset):
        updated = queryset.update(is_marked=True)
        self.message_user(request, f"{updated} user(s) marked.", level=messages.SUCCESS)
    mark_users.short_description = "Mark selected users"
    
    def unmark_users(self, request, queryset):
        updated = queryset.update(is_marked=False)
        self.message_user(request, f"{updated} user(s) unmarked.", level=messages.SUCCESS)
    unmark_users.short_description = "Unmark selected users"
    
    ##### Block a user from logging in
    def block_users(self, request, queryset):
        updated_count = queryset.update(is_blocked=True)
        messages.success(request, f"{updated_count} user(s) have been blocked.", level=messages.SUCCESS)
    block_users.short_description = "Block selected users"

    def unblock_users(self, request, queryset):
        updated_count = queryset.update(is_blocked=False)
        messages.success(request, f"{updated_count} user(s) have been unblocked.", level=messages.SUCCESS)
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
            new_password = get_random_string(
                8
            )  # Generate a random 8-character password
            user.set_password(new_password)
            user.save()
            user.email_user(
                subject="Your Password Has Been Reset",
                message=f"Your new password is: {new_password}\nPlease update it after logging in.",
            )
        messages.success(request, "Passwords have been reset and emailed to the users.")

    reset_passwords.short_description = "Reset passwords for selected users"
