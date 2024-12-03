from django.urls import include, path
from adminapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "adminapp"
urlpatterns = [
    path("user-profile", views.user_profile, name="user_profile"),
    path("account-summary", views.account_sumarry, name="account_summary"),
    path("transfer", views.transfer, name="transfer"),
    path("transfer-step1", views.transfer_step1, name="transfer_step1"),
    path("review-transaction", views.review_transaction, name="review_transaction"),
    path('verify-transaction', views.verify_transaction, name='verify_transaction'),
    path("transaction-successful", views.transaction_successful, name="transaction_successful",),
    path("deposit-check", views.deposit_check, name="deposit_check"),
    path("pay-bills", views.pay_bills, name="pay_bills"),
    path("add-card", views.add_card, name="add_card"),
    path("account-settings", views.account_settings, name="account_settings"),
    path("my-profile", views.my_profile, name="my_profile"),
    path("login-activity", views.login_activity, name="login_activity"),
]

