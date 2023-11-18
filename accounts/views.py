from .modules import *

# Create your views here

from .forms import LoginForm, SignUpForm, EmploymentInfo,ImageForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import State, Profile, User, Beneficiary_Security_Details
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy, reverse




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
                    request.session['cred'] = user.pk
                    return redirect("user/user-profile")
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
                    request.session['cred'] = user.pk
                    return redirect("/user-profile")
               else:    
                    msg = 'Invalid credentials'    
          else:
               msg = '' 
     return render(request, 'account_templates/login.html', {"form": form, "msg": msg})


    ##### Sign Up Views  #######
    ##### Sign Up Views
def enroll_step1(request):
     return render(request, 'account_templates/enroll_step1.html', {})

def enroll_step2(request):
     return render(request, 'account_templates/enroll_step2.html', {})



def enroll_step3(request):
     form = SignUpForm(request.POST or None)
     msg = ''

     if request.method == "POST" or "None":

          if form.is_valid():
               email = form.cleaned_data.get('email')
               first_name = form.cleaned_data.get('firstname')
               last_name = form.cleaned_data.get('lastname')
               middle_name = form.cleaned_data.get('middle_name')
               nick_name = form.cleaned_data.get('nick_name')
               date_of_birth = form.cleaned_data.get('date_of_birth')
               phone_number = form.cleaned_data.get('phone_number')
               residential_address = form.cleaned_data.get('residential_address')
               zip_code = form.cleaned_data.get('zip_code')
               account_type = form.cleaned_data.get('account_type')
               title = form.cleaned_data.get('title')
               gender = form.cleaned_data.get('gender')
               Currency_type = form.cleaned_data.get('Currency_type')
               state = form.cleaned_data.get('state')
               country = form.cleaned_data.get('country')
               city = form.cleaned_data.get('city')
               ssn = form.cleaned_data.get('ssn')


               # UserModel = 


               user = User.objects.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name
               )
               print(user)
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
                    return redirect('/enroll-step4/'+uid)
               else:
                    # No user    
                    msg = 'Something Went Wrong'            
          else:
               # form not valid
               msg = '' 
     return render(request, 'account_templates/enroll_step3.html',{"form": form, "msg" : msg})

def enroll_step4(request,uidb64):
     form = EmploymentInfo(request.POST or None)
     msg = ''

     if request.method == "POST" or "None":
          uid = urlsafe_base64_decode(uidb64).decode()

          if form.is_valid():
               password = form.cleaned_data.get('password')
               password_confirm = form.cleaned_data.get('password1')
               beneficiary_legal_name = form.cleaned_data.get('beneficiary_legal_name')
               nok_address = form.cleaned_data.get('nok_address')
               nok_relationship = form.cleaned_data.get('nok_relationship')
               nok_age = form.cleaned_data.get('nok_age')
               employment_type = form.cleaned_data.get('employment_type')
               salary_range = form.cleaned_data.get('salary_range')
               sq1_select = form.cleaned_data.get('sq1_select')
               sq1_answer = form.cleaned_data.get('sq1_answer')
               sq2_answer = form.cleaned_data.get('sq2_answer')
               sq2_select = form.cleaned_data.get('sq1_select')

               if password != password_confirm:
                    raise forms.ValidationError('Passwords do not match')
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
                    sq2_select=sq2_select
               )
               return redirect('/enroll-step5/'+uidb64)     
     return render(request, 'account_templates/enroll_step4.html', {"form": form, "msg": msg})

def send_activation_email(self, user):
        """Send activation email to user"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = reverse('accounts:activate_email', kwargs={
                                  'uidb64': uid, 'token': token})
        activation_url = self.request.build_absolute_uri(activation_url)
        context = {'user': user, 'activation_url': activation_url}
        message = render(
            self.request, 'accounts/activation_email.html', context)
        user.email_user(subject='Activate your account',
                         message=message.content.decode('utf-8'))



def enroll_step5(request, uidb64):
     form = ImageForm(request.POST, request.FILES)
     msg = ''
     uid = urlsafe_base64_decode(uidb64).decode()


     if request.method == "POST" or "None":

          if form.is_valid():
               UserModel = get_user_model()
               user = UserModel.objects.get(id=uid)
               if 'avatar' in request.FILES:
                    user.avatar = request.FILES['avatar']
                    user.save()
                    send_activation_email()
                    return redirect('/enroll-complete/'+uidb64)
               else:
                    msg = 'Picture could not be uploaded'    


     return render(request, 'account_templates/enroll_step5.html', {"form": form, "msg": msg})




def enroll_complete(request):
     return render(request, 'account_templates/enroll_complete.html', {})

# class enroll_complete(TemplateView):
#     """View upon successfull registration"""
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'accounts_templates/enroll_complete.html'
   
    
#     def post(self, request, *args, **kwargs):
#         """Handle post request"""
#         registration_form = UserRegistrationForm(self.request.POST)
#         address_form = UserAddressForm(self.request.POST)
#         if registration_form.is_valid() and address_form.is_valid():
#             user = registration_form.save(commit=False)
#             user.is_active = False
#             user.save()
#             address = address_form.save(commit=False)
#             address.user = user
#             address.save()
#             self.send_activation_email(user)
#             messages.success(
#                 self.request,
#                 (
#                     f'Thank You For Creating A Bank Account. '
#                     f'Please check your email to activate your account.'
#                 )
#             )
#             return HttpResponseRedirect(reverse_lazy('accounts:user_login'))
#         return self.render_to_response(
#             self.get_context_data(
#                 registration_form=registration_form,
#                 address_form=address_form
#             )
#         )

    

def LogoutView(request):
#     View for user logout
     if request.user.is_authenticated:
          logout(request)
     return redirect('/login')


def load_cities(request):
    country_id = request.GET.get('country_id')
    print(country_id)
    cities = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'account_templates/dropdown.html', {'cities': cities})
