from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Q
from accounts.models import Transfer, Deposit, VerificationCode
from itertools import chain
from datetime import datetime
from django.utils.timezone import now
from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import *
from .models import *


# Create your views here


@login_required(login_url="/login")
def user_profile(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)
    first_name = user.first_name[0] if user.first_name else ""
    last_name = user.last_name[0] if user.last_name else ""
    cad = cards.objects.filter(user_id=user)
    card_len = cad.count()

    dep = Deposit.objects.filter(user=user_id)

    trans = Transfer.objects.filter(user=user_id)
    account_data = list(chain(dep, trans))
    account_data.sort(key=lambda x: x.date, reverse=True)
    top_transactions = account_data[:20]
    return render(
        request,
        "user_templates/index.html",
        {
            "user": user,
            "account_data": top_transactions,
            "card": cad,
            "card_len": card_len,
        },
    )


@login_required(login_url="/login")
def account_sumarry(request):
    #### Retrive user's IP address
    user_id = request.session["cred"]
    userModel = get_user_model()

    user = userModel.objects.get(pk=user_id)

    dep = Deposit.objects.filter(user=user_id)
    trans = Transfer.objects.filter(user=user_id)

    account_data = list(chain(dep, trans))
    account_data.sort(key=lambda x: x.date, reverse=True)

    return render(
        request,
        "user_templates/account_summary.html",
        {"user": user, "account_data": account_data},
    )


@login_required(login_url="/login")
@csrf_exempt
def transfer(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)
    return render(request, "user_templates/transfer.html", {"user": user})


@login_required(login_url="/login")
# @csrf_exempt
def transfer_step1(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        formatted_amount = f"{float(amount):,.2f}"
        bank_name = request.POST.get("bankname")
        routing_number = request.POST.get("sortcode")
        account_number = request.POST.get("accountnumber")
        account_holder = request.POST.get("accountholder")
        description = request.POST.get("description")
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)
    return render(
        request,
        "user_templates/transfer_step1.html",
        {"user": user, "amount": amount, "formatted_amount": formatted_amount},
    )


@login_required(login_url="/login")
def review_transaction(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)

    if request.method == "POST":
        amount = request.POST.get("amount")
        formatted_amount = f"{float(amount):,.2f}"
        bank_name = request.POST.get("bankname")
        routing_number = request.POST.get("sortcode")
        account_number = request.POST.get("accountnumber")
        account_holder = request.POST.get("accountholder")
        description = request.POST.get("description")
        charge = 5 + int(amount)

        if user.bal > charge:
            # Generate a 6-digit random code
            verification_code = get_random_string(length=6, allowed_chars="0123456789")

            # Save or update the verification code in the database
            VerificationCode.objects.update_or_create(
                user=user,
                defaults={
                    "code": verification_code,
                    "created_at": now(),
                    "expires_at": now() + timedelta(minutes=10),
                },
            )

            # Send verification email
            subject = "Transaction Verification Code"
            context = {
                "user": user,
                "formatted_amount": formatted_amount,
                "bank_name": bank_name,
                "routing_number": routing_number,
                "account_number": account_number,
                "account_holder": account_holder,
                "description": description,
                "verification_code": verification_code,
                "full_name": f"{user.first_name} {user.last_name}",
            }
            html_message = render_to_string(
                "user_templates/transaction_code_email.html", context
            )
            plain_message = strip_tags(html_message)  # Fallback for non-HTML clients
            recipient_email = user.email

            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    html_message=html_message,
                    fail_silently=False,
                )

            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
                return redirect("user/transfer")

            # Save transaction details temporarily in the session
            request.session["transaction_data"] = {
                "amount": amount,
                "formatted_amount": formatted_amount,
                "bank_name": bank_name,
                "routing_number": routing_number,
                "account_number": account_number,
                "account_holder": account_holder,
                "description": description,
                "charge": charge,
            }

            return redirect("/user/review-transaction")

        else:
            messages.error(request, "Insufficient funds. Please deposit and try again.")
            return redirect("/user/user-profile")
    return render(
        request,
        "user_templates/review_transaction.html",
        {},
    )


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def verify_transaction(request):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        user = request.user
        code_entered = request.POST.get("verification_code")

        try:
            # Fetch the verification code for the user
            verification_entry = VerificationCode.objects.get(user=user)

            if (
                verification_entry.is_valid()
                and verification_entry.code == code_entered
            ):
                # Complete the transaction
                transaction_data = request.session.pop("transaction_data", None)
                if transaction_data:
                    # Deduct balance and save the transaction
                    user.bal -= transaction_data["charge"]
                    user.save()

                    Transfer.objects.create(
                        amount=transaction_data["amount"],
                        bank_name=transaction_data["bank_name"],
                        routing_number=transaction_data["routing_number"],
                        account_number=transaction_data["account_number"],
                        account_holder=transaction_data["account_holder"],
                        action=transaction_data["description"],
                        user=user,
                        status="Completed",
                    )

                    # Remove the used verification code
                    verification_entry.delete()

                    # Return a success response
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Transaction completed successfully!",
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Transaction data missing. Please try again.",
                        },
                        status=400,
                    )
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid or expired verification code.",
                    },
                    status=400,
                )
        except VerificationCode.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No verification code found for this user.",
                },
                status=404,
            )

    return JsonResponse(
        {
            "status": "error",
            "message": "Invalid request method or not an AJAX request.",
        },
        status=400,
    )


@login_required(login_url="/login")
def transaction_successful(request):
    user = request.user
    # Fetch the most recent transaction
    data = Transfer.objects.filter(user=user).order_by("-date").first()
    return render(request, "user_templates/transaction_successful.html", {"data": data})


# @login_required(login_url="/login")
# def review_transaction(request):
#     user_id = request.session['cred']
#     userModel = get_user_model()
#     user = userModel.objects.get(pk=user_id)

#     if request.method=="POST":
#         amount = request.POST.get('amount')
#         formatted_amount = f"{float(amount):,.2f}"
#         bank_name = request.POST.get('bankname')

#         routing_number = request.POST.get('sortcode')
#         account_number = request.POST.get('accountnumber')
#         account_holder = request.POST.get('accountholder')
#         description = request.POST.get('description')
#         charge = 5 + int(amount)

#         if user.bal > charge:
#             current_bal = user.bal - charge
#             user.bal = current_bal
#             user.save()
#             resolve = Transfer.objects.create(
#                 amount=amount,
#                 bank_name=bank_name,
#                 routing_number=routing_number,
#                 account_number=account_number,
#                 account_holder=account_holder,
#                 action=description,
#                 user = user
#             )

#         else:
#             messages.error(
#                 request,
#                 (
#                     f'Insufficient Funds. '
#                     f'Make some deposit to your account and try again.'

#                 ))
#             return redirect('/user/user-profile')
#     return render(request, 'user_templates/review_transaction.html',{"amount":amount,"formatted_amount":formatted_amount, "bank_name":bank_name,"routing_number":routing_number,"account_number":account_number,"account_holder":account_holder,"description":description})


# @login_required(login_url="/login")
# @csrf_exempt
# def transaction_successful(request):
#     user_id = request.session['cred']
#     userModel = get_user_model()
#     user = userModel.objects.get(pk=user_id)
#     data = Transfer.objects.filter(user=user_id).order_by('date').last()

#     return render(request, 'user_templates/transaction_successful.html',{'data':data})


@login_required(login_url="/login")
def deposit_check(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)

    form = Check_DepositForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

            if "front_check" and "back_check" in request.FILES:
                front_check = request.FILES["front_check"]
                back_check = request.FILES["back_check"]
                amount = form.cleaned_data.get("amount")

                DepositCheck.objects.create(
                    front_check=front_check,
                    back_check=back_check,
                    amount=amount,
                    user=user,
                )
                form = Check_DepositForm()
                messages.success(request, (f"Check Uploaded Successfully. "))
        else:
            messages.error(request, (f"Check upload not Successful. "))

    return render(
        request, "user_templates/deposit_check.html", {"user": user, "form": form}
    )


@login_required(login_url="/login")
def pay_bills(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)
    bill_params = paybills.objects.filter(user=user_id).order_by("date")

    form = addNewBillerForm(request.POST or None, request)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")
            payment_method = form.cleaned_data.get("payment_method")
            account_number = form.cleaned_data.get("account_number")
            address1 = form.cleaned_data.get("address1")
            address2 = form.cleaned_data.get("address2")
            city = form.cleaned_data.get("city")
            state = form.cleaned_data.get("state")
            zip_code = form.cleaned_data.get("zip_code")
            nickname = form.cleaned_data.get("nickname")

            paybillUser.objects.create(
                name=name,
                payment_method=payment_method,
                account_number=account_number,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                zip_code=zip_code,
                nickname=nickname,
                user=user,
            )
            form = addNewBillerForm(request.POST or None)
            messages.success(request, (f"Successfully Added {name} to Biller List. "))
        else:
            messages.error(request, (f"Add new Biller not Successful. "))

    formtwo = payBillByUser(request.user, request.POST or None)
    if request.method == "POST":
        if formtwo.is_valid():
            amount = formtwo.cleaned_data.get("amount")
            delivery_date = formtwo.cleaned_data.get("delivery_date")
            action = formtwo.cleaned_data.get("action")
            paid_to = formtwo.cleaned_data.get("paid_to")

            paybills.objects.create(
                amount=amount,
                delivery_date=delivery_date,
                action=action,
                paid_to=paid_to,
                user=user,
            )
            formtwo = payBillByUser()
            messages.success(request, (f"Successfully sent {amount} to {paid_to}. "))

        else:
            messages.error(request, (f"Transaction Not successful. "))

    return render(
        request,
        "user_templates/pay_bills.html",
        {"bill": bill_params, "form": form, "formtwo": formtwo},
    )


@login_required(login_url="/login")
def add_card(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)

    form = addCardForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")
            card_number = form.cleaned_data.get("card_number")
            cvv = form.cleaned_data.get("cvv")
            expiry_month = request.POST.get("month")
            expiry_year = request.POST.get("year")

            cards.objects.create(
                name=name,
                card_number=card_number,
                cvv=cvv,
                expiry_month=expiry_month,
                expiry_year=expiry_year,
                user=user,
            )
            form = addCardForm()
            messages.success(request, (f"Card successfully linked. "))
        else:
            messages.error(request, (f"Card linking not Successful. "))

    else:
        form = addCardForm()

    return render(request, "user_templates/add_card.html", {"user": user, "form": form})


@login_required(login_url="/login")
def account_settings(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)
    logs = loginActivity.objects.filter(user=user_id).reverse().order_by("time")[:3]

    form = setNewPasswordForm(request.POST or None)

    if request.method == "POST" or "None":
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            form = setNewPasswordForm()
            messages.success(request, (f"Password Changed successfully. "))
        else:
            messages.error(request, (f"Password Change not successful. "))

    return render(
        request,
        "user_templates/account_settings.html",
        {"user": user, "form": form, "logs": logs},
    )


@login_required(login_url="/login")
def my_profile(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)
    return render(request, "user_templates/my_profile.html", {"user": user})


@login_required(login_url="/login")
def login_activity(request):
    user_id = request.session["cred"]
    userModel = get_user_model()
    user = userModel.objects.get(pk=user_id)

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"

    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string

    context = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version": os_version,
    }

    loginActivity.objects.create(
        ip=ip,
        device_type=device_type,
        browser_type=browser_type,
        browser_version=browser_version,
        os_type=os_type,
        os_version=os_version,
        user=user,
    )

    logs = loginActivity.objects.filter(user=user_id).reverse().order_by("time")

    return render(
        request,
        "user_templates/login_activity.html",
        {"activity": context, "logs": logs},
    )
