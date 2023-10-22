from .modules import *

# Create your views here

from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth import get_user_model



# Create your views here
def index(request):
     form = LoginForm(request.POST or None)

     msg = None

     if request.method == "POST" or "None":

          if form.is_valid():
               username = form.cleaned_data.get("account_number")
               password = form.cleaned_data.get("password")
               
          
               UserModel = get_user_model()
               user = UserModel.objects.get(account_number=username)
               
               login_valid = user == username
               # user = authenticate(username=username, password=password)
               
               if login_valid is not None:
                    login(request, user)
                    return redirect("/user-profile")
               else:    
                    msg = 'Invalid credentials'    
          else:
               msg = '' 
          return render(request, 'account_templates/index.html',{"form": form, "msg" : msg})




# def register_user(request):

#     msg     = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)
#             profile.objects.create(user=user)
            

#             msg     = 'User created - please login.'
#             success = True
            
#             return redirect("/login/")

#         else:
#             msg = 'Form is not valid'    
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


    ##### Sign Up Views
def enroll_step1(request):
     return render(request, 'account_templates/enroll_step1.html', {})

def enroll_step2(request):
     return render(request, 'account_templates/enroll_step2.html', {})

def enroll_step3(request):
     return render(request, 'account_templates/enroll_step3.html', {})
     return render(request, 'account_templates/online_registration.html', {})

def enroll_step2(request):
     return render(request, 'account_templates/terms_conditions.html', {})
