from django.urls import include, path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static 

app_name = 'accounts'

urlpatterns = [
path('', views.index, name='index'),
path('capital-funding-account', views.capitalfunding_account, name='capitalfunding_account'),
path('advanced-account', views.advanced_account, name='advanced_account'),
path('student-account', views.student_account, name='student_account'),
path('bank-account', views.bank_account, name='bank_account'),

       ###########          ###########
          ##     sign up urls  ##
       ###########          ###########
path('login', views.login_user, name='login'),
path('logout', views.LogoutView, name='logout'),
path('enroll-step1', views.enroll_step1, name='enroll_step1'),
path('enroll-step2', views.enroll_step2, name='enroll_step2'),
path('enroll-step3', views.enroll_step3, name='enroll_step3'),
path('enroll-step4/<str:uidb64>', views.enroll_step4, name='enroll_step4'),
path('enroll-step5/<str:uidb64>', views.enroll_step5, name='enroll_step5'),
path('enroll-complete/<str:uidb64>', views.enroll_complete, name='enroll_complete'),
path('query/load-cities/', views.load_cities, name='query_load_cities'),
]
