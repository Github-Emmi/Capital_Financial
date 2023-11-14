from django.shortcuts import render

# Create your views here
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here
@login_required(login_url="/login/")
def user_profile(request):
     user_id = request.session['cred']
     userModel = get_user_model()
     user = userModel.objects.get(pk=user_id)
     
     
     return render(request, 'user_templates/index.html', {"user": user})