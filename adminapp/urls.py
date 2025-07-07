from django.urls import include, path
from adminapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "adminapp"
urlpatterns = [
    path("user-profile", views.user_profile, name="user_profile"),
    path("account-summary", views.account_sumarry, name="account_summary"),
    path("transfer", views.transfer, name="transfer"),
    path('fetch-account-details/', views.fetch_account_details, name='fetch_account_details'),
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





#################################  transaction_successful.html ################
# {% extends 'user_templates/base.html' %}
# {% load static %}
# {% block main_content %}


# <div class="nk-content nk-content-fluid">
#     <div class="container-xl wide-lg">
#      <div class="nk-content-body">
#    <div class="modal-content">
#       <div class="modal-body modal-body-lg text-center">
#           <div class="nk-modal">
#               <em class="nk-modal-icon icon icon-circle icon-circle-xxl ni ni-check bg-success"></em>
#               <h4 class="nk-modal-title">Transaction successful!</h4>
#               <div class="nk-modal-text">
#                   <p class="caption-text">You have successfully transfered <strong>{{data.amount}}</strong> USD to <strong>{{data.account_holder}}</strong>.</p>
#                  <p class="sub-text-sm"></p>
#                  <b>Details of your transaction are shown below;</b>
#               </div>
#               <ul class="buysell-overview-list">
#                       <li class="buysell-overview-item">
#                       <span class="pm-currency"><em class="icon ni ni-check-circle-fill"></em> <span>Amount Debited</span></span>
#                           <span class="pm-title">USD {{data.amount}}</span>
#                       </li>
#                        <li class="buysell-overview-item">
#                       <span class="pm-currency"><em class="icon ni ni-check-circle-fill"></em> <span>Transaction refrence:</span></span>
#                           <span class="pm-title">CAP/{{data.txnId}}</span>
            
#                       </li>

#                       <li class="buysell-overview-item">
#                       <span class="pm-currency"><em class="icon ni ni-check-circle-fill"></em> <span>Account holder:</span></span>
#                           <span class="pm-title">{{data.account_holder}}</span>
#                       </li>

#                       <li class="buysell-overview-item">
#                       <span class="pm-currency"><em class="icon ni ni-check-circle-fill"></em> <span>Bank Name:</span></span>
#                           <span class="pm-title">{{data.bank_name}}</span>
#                       </li>

#                       <li class="buysell-overview-item">
#                       <span class="pm-currency"><em class="icon ni ni-check-circle-fill"></em> <span>Date:</span></span>
#                           <span class="pm-title">{% now "d F Y H:i" %}</span>
#                       </li>

#                       <li class="buysell-overview-item">
#                       <span class="pm-currency"><em class="icon ni ni-check-circle-fill"></em> <span>Available Balance:</span></span>
#                           <span class="pm-title">USD {{user.bal}}</span>
#                       </li>


#                   </ul>
#               <div class="nk-modal-action-lg">
#                   <ul class="btn-group gx-4">
#                       <li><a href="{% url 'adminapp:transfer' %}" class="btn btn-lg btn-mw btn-primary">New transaction</a></li>
#                       <li><a href="{% url 'adminapp:user_profile' %}" class="btn btn-lg btn-mw btn-secondary">Back to home</a></li>
#                   </ul>
#               </div>
#           </div>
#       </div><!-- .modal-body -->
#       <div class="modal-footer bg-lighter">
#           <div class="text-center w-100">
#               <p>All electronic fund transfers to or from your accounts at Capital Financial Union are governed by the Electronic Fund Transfer Disclosure provided to you when you established your account or when you requested other electronic fund transfer services.</p>
#           </div>
#       </div>
#   </div>
# </div>
# </div>
# </div>

# {% endblock main_content%}