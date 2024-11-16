from django.db import models
from django.conf import settings
import uuid
from accounts.choices import Status, payment_method

# Create your models here.

class DepositCheck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    front_check = models.ImageField(upload_to='checkfront/', null=True, blank=True)
    back_check = models.ImageField(upload_to='checkback/', null=True, blank=True)
    amount = models.CharField(max_length=30)
    

class cards(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(('cardholder name'), max_length=30)
    card_number = models.IntegerField(('card number'))
    cvv = models.IntegerField(('card cvv'))
    expiry_month = models.CharField(('card expiry month'), max_length=30, blank=True)
    expiry_year = models.CharField(('card expiry year'), max_length=30, blank=True)



class loginActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    browser_type = models.CharField(max_length=100)
    browser_version = models.CharField(max_length=100)
    os_type = models.CharField(max_length=100)
    os_version = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    

class paybillUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50, choices=payment_method)
    account_number = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50)
    state= models.CharField(max_length=50)
    zip_code = models.PositiveIntegerField(('zip code'))
    nickname = models.CharField(max_length=50,blank=True)


    def __str__(self):
        return self.name 

    



class paybills(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paid_to = models.ForeignKey(paybillUser, on_delete=models.CASCADE)
    txnId = models.UUIDField(default=uuid.uuid4, editable=False)
    txnType = models.CharField(max_length=10,default="Debit", editable=False)
    amount = models.CharField(max_length=30)
    delivery_date = models.DateField()
    action = models.CharField(max_length=30,blank=True)
    status = models.CharField(max_length=50, choices=Status, default='Successful')
    date = models.DateTimeField(auto_now_add=True)
    


    # def __str__(self):
    #     return f'Transfer details  {self.txnId}'
