from django.urls import include, path
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static 


app_name = 'accounts'

urlpatterns = [
path('', index, name='index'),
path('capital-funding-account', capitalfunding_account, name='capitalfunding_account'),
path('advanced-account', advanced_account, name='advanced_account'),
path('student-account', student_account, name='student_account'),
path('bank-account', bank_account, name='bank_account'),
path('accounts/activate/<str:uidb64>',
         activate_email, name='activate_email'),

       ###########          ###########
          ##     sign up urls  ##
       ###########          ###########
path('login', login_user, name='login'),
path('logout', LogoutView, name='logout'),
path('enroll-step1', enroll_step1, name='enroll_step1'),
path('enroll-step2', enroll_step2, name='enroll_step2'),
path('enroll-step3', enroll_step3, name='enroll_step3'),
path('enroll-step4/<str:uidb64>', enroll_step4, name='enroll_step4'),
path('enroll-step5/<str:uidb64>', enroll_step5, name='enroll_step5'),
path('enroll-complete/<str:uidb64>', enroll_complete, name='enroll_complete'),
path('query/load-cities/', load_cities, name='query_load_cities'),
path("forgot-password", forgot_password, name="forgot_password"),
]


