from django.shortcuts import render

# Create your views here
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here
@login_required(login_url="/login")
def user_profile(request):     
     user_id = request.session['cred']
     userModel = get_user_model()
     user = userModel.objects.get(pk=user_id)
     
     
     return render(request, 'user_templates/index.html', {"user": user})

@login_required(login_url="/login")
def account_sumarry(request):
    #### Retrive user's IP address
    


    return render(request, 'user_templates/account_summary.html', {})

@login_required(login_url="/login")
def transfer(request):
    return render(request, 'user_templates/transfer.html', {})

@login_required(login_url="/login")
def transfer_step1(request):
    return render(request, 'user_templates/transfer_step1.html', {})

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