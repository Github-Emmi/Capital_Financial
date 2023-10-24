from django.urls import path
from accounts import views, users

app_name = 'accounts'

urlpatterns = [
path('', views.index, name='index'),
path('user-profile', users.user_profile, name='user_profile'),
       ###########          ###########
          ##     sign up urls  ##
       ###########          ###########
path('login', views.login_user, name='login'),
path('enroll-step1', views.enroll_step1, name='enroll_step1'),
path('enroll-step2', views.enroll_step2, name='enroll_step2'),
path('enroll-step3', views.enroll_step3, name='enroll_step3'),
path('enroll-step4', views.enroll_step4, name='enroll_step4'),
path('enroll-step5', views.enroll_step5, name='enroll_step5'),
path('enroll-complete', views.enroll_complete, name='enroll_complete'),
]