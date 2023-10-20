from django.shortcuts import render
<<<<<<< HEAD

# Create your views here
=======
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required(login_url="/login/")
>>>>>>> 27d17dc (auth workflow)
def user_profile(request):
     return render(request, 'user_templates/index.html', {})