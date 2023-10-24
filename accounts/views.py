from .modules import *

# Create your views here
def index(request):
     return render(request, 'account_templates/index.html', {})

def login(request):
     return render(request, 'account_templates/login.html')


    ##### Sign Up Views  #######
def enroll_step1(request):
     return render(request, 'account_templates/enroll_step1.html', {})

def enroll_step2(request):
     return render(request, 'account_templates/enroll_step2.html', {})

def enroll_step3(request):
     return render(request, 'account_templates/enroll_step3.html', {})

def enroll_step4(request):
     return render(request, 'account_templates/enroll_step4.html', {})

def enroll_step5(request):
     return render(request, 'account_templates/enroll_step5.html', {})

def enroll_complete(request):
     return render(request, 'account_templates/enroll_complete.html', {})