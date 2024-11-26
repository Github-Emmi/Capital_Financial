from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from venexapp.models import User


def account_dashboard(request):
    return render(request, "admin_templates/account.html")


def deposit_list(request):
    return render(request, "admin_templates/deposit-list.html")


def earning_history(request):
    return render(request, "admin_templates/earning-history.html")


def security(request):
    return render(request, "admin_templates/security.html")


def edit_account(request):
    return render(request, "admin_templates/edit-account.html")


def add_clients(request):
    return render(request, "admin_templates/add-clients.html")


def save_clients(request):

    if request.method != "POST":
        HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                user_type=2,
            )
            user.clients.address = address
            user.save()
            messages.success(request, "Successfully Added Staff.")
            return HttpResponseRedirect("/add-clients")
        except:
            messages.error(request, "failed To Add Staff.")
            return HttpResponseRedirect("/add-clients")
