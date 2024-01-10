from django.shortcuts import render

# Create your views here
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Transfer, User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here
@login_required(login_url="/login")
def user_profile(request):     
     user_id = request.session['cred']
     userModel = get_user_model()
     user = userModel.objects.get(pk=user_id)
     first_name = user.first_name[0] if user.first_name else ''
     last_name = user.last_name[0] if user.last_name else ''
     
     
     return render(request, 'user_templates/index.html', {"user": user, 'first_name':first_name,'last_name':last_name,})

@login_required(login_url="/login")
def account_sumarry(request):
    #### Retrive user's IP address
    
    return render(request, 'user_templates/account_summary.html', {})

@login_required(login_url="/login")
@csrf_exempt
def transfer(request):

    return render(request, 'user_templates/transfer.html', {})

@login_required(login_url="/login")
# @csrf_exempt
def transfer_step1(request):
    if request.method=="POST":
        amount = request.POST.get('amount')
        bank_name = request.POST.get('bankname')
        routing_number = request.POST.get('sortcode')
        account_number = request.POST.get('accountnumber')
        account_holder = request.POST.get('accountholder')
        description = request.POST.get('description')
    return render(request, 'user_templates/transfer_step1.html', {'amount':amount})    

@login_required(login_url="/login")
def review_transaction(request):

    return render(request, 'user_templates/review_transaction.html',)    

@login_required(login_url="/login")
def transasction_successful(request):
    return render(request, 'user_templates/transaction_successful.html', {})
    
@login_required(login_url="/login")
def deposit_check(request):
    return render(request, 'user_templates/deposit_check.html', {})

@login_required(login_url="/login")
def pay_bills(request):
    return render(request, 'user_templates/pay_bills.html', {})

@login_required(login_url="/login")
def add_card(request):
    return render(request, 'user_templates/add_card.html', {})

@login_required(login_url="/login")
def account_settings(request):
    return render(request, 'user_templates/account_settings.html', {})

@login_required(login_url="/login")
def my_profile(request):
    return render(request, 'user_templates/my_profile.html', {})

@login_required(login_url="/login")
def login_activity(request):
    return render(request, 'user_templates/login_activity.html', {})