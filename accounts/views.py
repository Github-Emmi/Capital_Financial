from .modules import *
from .forms import LoginForm, SignUpForm, EmploymentInfo, ImageForm, forgotPassForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import State, Profile, User, Beneficiary_Security_Details
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils.encoding import force_str


# Create your views here
def index(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST" or "None":

        if form.is_valid():
            username = form.cleaned_data.get("account_number")
            password = form.cleaned_data.get("password")
            UserModel = get_user_model()
            user_mail = UserModel.objects.get(account_number=username)

            user = authenticate(email=user_mail, password=password)

            if user is not None:
                login(request, user)
                request.session["cred"] = user.pk
                return redirect("/user/user-profile")
            else:
                msg = "Invalid credentials"
        else:
            msg = ""
        return render(
            request, "account_templates/index.html", {"form": form, "msg": msg}
        )


def capitalfunding_account(request):
    return render(request, "account_templates/capitalfunding_account.html", {})


def advanced_account(request):
    return render(request, "account_templates/advanced_account.html", {})


def student_account(request):
    return render(request, "account_templates/student_account.html", {})


def bank_account(request):
    return render(request, "account_templates/bank_account.html", {})


def login_user(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST" or "None":
        if form.is_valid():
            username = form.cleaned_data.get("account_number")
            password = form.cleaned_data.get("password")
            UserModel = get_user_model()
            user_mail = UserModel.objects.get(account_number=username)
            user = authenticate(email=user_mail, password=password)

            if user is not None:
                login(request, user)
                request.session["cred"] = user.pk
                return redirect("/user/user-profile")
            else:
                msg = "Invalid credentials"
        else:
            msg = ""
    return render(request, "account_templates/login.html", {"form": form, "msg": msg})


def account_blocked(request):
    if request.user.is_authenticated and request.user.is_blocked:
        return render(
            request,
            "account_templates/account_blocked.html",
            {
                "user": request.user,
                "date_flagged": request.user.date_flagged,
            },
        )
    return redirect("/user/user-profile")  # Redirect non-blocked users to home

    ##### Sign Up Views  #######
    ##### Sign Up Views


def enroll_step1(request):
    return render(request, "account_templates/enroll_step1.html", {})


def enroll_step2(request):
    return render(request, "account_templates/enroll_step2.html", {})


def enroll_step3(request):
    form = SignUpForm(request.POST or None)
    msg = ""

    if request.method == "POST" or "None":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("firstname")
            last_name = form.cleaned_data.get("lastname")
            middle_name = form.cleaned_data.get("middle_name")
            nick_name = form.cleaned_data.get("nick_name")
            date_of_birth = form.cleaned_data.get("date_of_birth")
            phone_number = form.cleaned_data.get("phone_number")
            residential_address = form.cleaned_data.get("residential_address")
            zip_code = form.cleaned_data.get("zip_code")
            account_type = form.cleaned_data.get("account_type")
            title = form.cleaned_data.get("title")
            gender = form.cleaned_data.get("gender")
            Currency_type = form.cleaned_data.get("Currency_type")
            state = form.cleaned_data.get("state")
            country = form.cleaned_data.get("country")
            city = form.cleaned_data.get("city")
            ssn = form.cleaned_data.get("ssn")
            user = User.objects.create(
                email=email, first_name=first_name, last_name=last_name
            )

            if user:
                # state,country,dob,
                Profile.objects.create(
                    user=user,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    account_type=account_type,
                    middle_name=middle_name,
                    nick_name=nick_name,
                    city=city,
                    zip_code=zip_code,
                    phone_number=phone_number,
                    Currency_type=Currency_type,
                    state=state,
                    country=country,
                    residential_address=residential_address,
                    title=title,
                )
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print(uid)
                print(user.pk)
                return redirect("/enroll-step4/" + uid)
            else:
                # No user
                msg = "Something Went Wrong"
        else:
            # form not valid
            msg = ""
    return render(
        request, "account_templates/enroll_step3.html", {"form": form, "msg": msg}
    )


def enroll_step4(request, uidb64):
    form = EmploymentInfo(request.POST or None)
    msg = ""

    if request.method == "POST" or "None":
        uid = urlsafe_base64_decode(uidb64).decode()

        if form.is_valid():
            password = form.cleaned_data.get("password")
            password_confirm = form.cleaned_data.get("password1")
            beneficiary_legal_name = form.cleaned_data.get("beneficiary_legal_name")
            nok_address = form.cleaned_data.get("nok_address")
            nok_relationship = form.cleaned_data.get("nok_relationship")
            nok_age = form.cleaned_data.get("nok_age")
            employment_type = form.cleaned_data.get("employment_type")
            salary_range = form.cleaned_data.get("salary_range")
            sq1_select = form.cleaned_data.get("sq1_select")
            sq1_answer = form.cleaned_data.get("sq1_answer")
            sq2_answer = form.cleaned_data.get("sq2_answer")
            sq2_select = form.cleaned_data.get("sq1_select")

            if password != password_confirm:
                raise form.ValidationError("Passwords do not match")
                # msg = 'Passwords do not match'

            # print(form.cleaned_data)
            UserModel = get_user_model()
            user = UserModel.objects.get(id=uid)
            user.set_password(password)
            user.save()
            Beneficiary_Security_Details.objects.create(
                user=user,
                beneficiary_legal_name=beneficiary_legal_name,
                nok_address=nok_address,
                nok_relationship=nok_relationship,
                nok_age=nok_age,
                employment_type=employment_type,
                salary_range=salary_range,
                sq1_select=sq1_select,
                sq1_answer=sq1_answer,
                sq2_answer=sq2_answer,
                sq2_select=sq2_select,
            )
            return redirect("/enroll-step5/" + uidb64)
    return render(
        request, "account_templates/enroll_step4.html", {"form": form, "msg": msg}
    )


def activate_email(request, uidb64, token):
    """View to activate user account"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now login.")
    else:
        messages.error(request, "Invalid activation link.")
    return HttpResponseRedirect(reverse_lazy("accounts:user_login"))


def enroll_step5(request, uidb64):
    form = ImageForm(request.POST, request.FILES)
    msg = ""
    uid = urlsafe_base64_decode(uidb64).decode()

    if request.method == "POST" or "None":

        if form.is_valid():
            UserModel = get_user_model()
            user = UserModel.objects.get(id=uid)
            if "avatar" in request.FILES:
                user.avatar = request.FILES["avatar"]
                user.save()

                # Send Welcome Email
                subject = "Welcome to Our Banking Platform!"
                context = {
                    "user": user,
                    "full_name": f"{user.first_name} {user.last_name}",
                }
                html_message = render_to_string(
                    "account_templates/welcome_email.html", context
                )
                plain_message = strip_tags(
                    html_message
                )  # Fallback for non-HTML clients

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )

                return redirect("/enroll-complete/" + uidb64)
            else:
                msg = "Picture could not be uploaded"

    return render(
        request, "account_templates/enroll_step5.html", {"form": form, "msg": msg}
    )


def enroll_complete(request, uidb64):
    uid = urlsafe_base64_decode(uidb64).decode()
    UserModel = get_user_model()
    user = UserModel.objects.get(id=uid)

    return render(request, "account_templates/enroll_complete.html", {"user": user})


def verify_email(request, uidb64, token):
    """Verifies the user's email and sends a follow-up email."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Send follow-up email
        send_mail(
            "Email Verified",
            "Your email has been successfully verified. Welcome to Capital Financial!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "Your email has been verified successfully.")
        return redirect("login")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("")


def forgot_password(request):
    form = forgotPassForm(request.POST or None)
    return render(request, "account_templates/forgot_password.html", {"form": form})


def LogoutView(request):
    #     View for user logout
    if request.user.is_authenticated:
        logout(request)
    return redirect("/login")


def load_cities(request):
    country_id = request.GET.get("country_id")
    cities = State.objects.filter(country_id=country_id).order_by("name")
    return render(request, "account_templates/dropdown.html", {"cities": cities})
