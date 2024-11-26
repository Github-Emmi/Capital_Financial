from django.db import models

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

# Create your models here.
amount = (
    ('none', 'Select Amount'),
    ('100', '100'),
    ('500', '500'),
    ('600', '600'),
    ('1000', '1,000'),
    ('2000', '2,000'),
    ('5000', '5,000'),
)

method = (
    ('none', 'Select Method'),
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('USDT', 'USDTCoin'),
    ('TR', 'Tron'),
    ('LTC', 'LiteCoin'),
)

class CustomUser(AbstractUser):
    user_type_data = ((1, "User"), (2, "Client"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length= 30)
    fund_amount = models.CharField(max_length=15, choices=amount, default='none')
    withdrawal_method = models.CharField(max_length=15, choices=method, default='none')

    # Additional fields here  
    groups = models.ManyToManyField(  
        'auth.Group',  
        related_name='venexapp_customuser_set',  # Change this to a unique name  
        blank=True,  
        help_text='The groups this user belongs to.',  
        related_query_name='user',  
    )  

    user_permissions = models.ManyToManyField(  
        'auth.Permission',  
        related_name='venexapp_customuser_permissions_set',  # Change this to a unique name  
        blank=True,  
        help_text='Specific permissions for this user.',  
        related_query_name='user',  
    )  
    

class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    btc_wallet = models.CharField(max_length=30, blank=True)
    Ethereum_wallet = models.CharField(max_length=30, blank=True)
    USDT_wallet = models.CharField(max_length=30, blank=True)
    Litecoin_wallet = models.CharField(max_length=30, blank=True)
    tron_wallet = models.CharField(max_length=30, blank=True)
    phone_no = models.CharField(max_length=25, blank=True)
    profile_pic = models.FileField() 
    gender = models.CharField(max_length= 225)
    address = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    profile_pic = models.FileField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()    

class NotificationClients(models.Model):
    id = models.AutoField(primary_key=True)
    clients_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notified = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    
    
    

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(admin=instance,address="",profile_pic="",btc_wallet="",Ethereum_wallet="",
                                     Litecoin_wallet="",tron_wallet="",phone_no="", USDT_wallet="",gender="")
        if instance.user_type==2:
            Clients.objects.create(admin=instance, address="", profile_pic="",)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminuser.save()
    if instance.user_type==2:
        instance.clients.save()                     