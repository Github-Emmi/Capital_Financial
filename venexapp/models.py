# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from accounts.models import User

# Create your models here.
amount = (
    ("none", "Select Amount"),
    ("100", "100"),
    ("500", "500"),
    ("600", "600"),
    ("1000", "1,000"),
    ("2000", "2,000"),
    ("5000", "5,000"),
)

method = (
    ("none", "Select Method"),
    ("BTC", "Bitcoin"),
    ("ETH", "Ethereum"),
    ("USDT", "USDTCoin"),
    ("TR", "Tron"),
    ("LTC", "LiteCoin"),
)

class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    btc_wallet = models.CharField(max_length=30, blank=True)
    ethereum_wallet = models.CharField(max_length=30, blank=True)
    usdt_wallet = models.CharField(max_length=30, blank=True)
    litecoin_wallet = models.CharField(max_length=30, blank=True)
    tron_wallet = models.CharField(max_length=30, blank=True)
    phone_no = models.CharField(max_length=25, blank=True)
    profile_pic = models.FileField(blank=True)
    gender = models.CharField(max_length=225, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Admin: {self.admin.get_full_name()}"


class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    profile_pic = models.FileField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client: {self.admin.get_full_name()}"



class NotificationClients(models.Model):
    id = models.AutoField(primary_key=True)
    clients_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notified = models.DateTimeField(default=timezone.now)
    objects = models.Manager()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:  # Admin
            AdminUser.objects.create(admin=instance)
        elif instance.user_type == 2:  # Client
            Clients.objects.create(admin=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1 and hasattr(instance, 'adminuser'):
        instance.adminuser.save()
    elif instance.user_type == 2 and hasattr(instance, 'clients'):
        instance.clients.save()