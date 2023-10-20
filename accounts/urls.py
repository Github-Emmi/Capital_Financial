from django.urls import path
from accounts import views, users

app_name = 'accounts'

urlpatterns = [
path('', views.index, name='index'),
path('user-profile', users.user_profile, name='user_profile'),
       ###########          ###########
          ##     sign up urls  ##
       ###########          ###########
path('enroll-step1', views.enroll_step1, name='enroll_step1'),
path('enroll-step2', views.enroll_step2, name='enroll_step2'),
<<<<<<< HEAD
path('enroll-step3', views.enroll_step3, name='enroll_step3'),
=======
>>>>>>> 27d17dc (auth workflow)
]