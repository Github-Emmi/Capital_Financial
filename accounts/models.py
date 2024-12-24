# Create your models here.
from __future__ import unicode_literals
import uuid
from django.db import models
import random
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from .choices import Title,Employment,Gender,Status,Salary,Account_Type,nok_Age,Security_Question_One,Security_Question_Two,Currency,nok_relationship
from django.core.mail import EmailMessage, get_connection
from django.utils.html import format_html



# custom user and manager area
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser') or not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_superuser=True and is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=30)
    date_joined = models.DateTimeField(('date joined'), default=now)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='uploads/', null=True, blank=True)
    account_number = models.BigIntegerField(('account_number'), unique=True, blank=True, null=True)
    bal = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    is_blocked = models.BooleanField(default=False)
    date_flagged = models.DateTimeField(('date flagged'), null=True, blank=True)

    # Fields for roles (Venex App)
    USER_TYPE_CHOICES = ((1, "User"), (2, "Client"))
    user_type = models.IntegerField(default=1, choices=USER_TYPE_CHOICES)
    fund_amount = models.CharField(max_length=15, choices=[("none", "None"), ("low", "Low"), ("high", "High")], default="none")
    withdrawal_method = models.CharField(max_length=15, choices=[("none", "None"), ("bank", "Bank"), ("crypto", "Crypto")], default="none")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return f"{self.first_name[:1]} {self.last_name[:1]}".strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            email = EmailMessage(subject, message, from_email, [self.email], connection=connection, **kwargs)
            email.send()

    @property
    def formatted_balance(self):
        return f"{self.bal:,.2f}"

@receiver(post_save, sender=User)  
def create_author(sender, instance, created, **kwargs):  
    if created:  
        # Generate a random 10-digit number that is unique  
        while True:  
            account_number = random.randint(1000000000, 9999999999)  # Generate 10-digit account number  
            if not User.objects.filter(account_number=account_number).exists():  # Ensure uniqueness  
                break  
        User.objects.filter(pk=instance.id).update(account_number=account_number)  
        
class Country(models.Model):
    id = models.IntegerField(primary_key=True)  # Explicit primary key to match CSV
    name = models.CharField(('country name'), max_length=55, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"

class State(models.Model):
    id = models.IntegerField(primary_key=True)  # Explicit primary key to match CSV
    name = models.CharField(('state name'), max_length=55)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "States"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(('last name'), max_length=30)
    nick_name = models.CharField(('nick name'), max_length=30)
    date_of_birth = models.DateField(('date of birth'), max_length=30)
    zip_code = models.PositiveIntegerField(('zip code'))
    residential_address = models.CharField(('residential address'), max_length=300)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(('city'),max_length=55)
    ssn = models.CharField(('ssn'), max_length=30)
    phone_number = models.CharField(('phone number'), max_length=30)
    
    title = models.CharField(max_length=17, choices=Title, default='none')
    gender = models.CharField(max_length=17, choices=Gender, default='none')
    account_type = models.CharField(max_length=37, choices=Account_Type, default='none')
    Currency_type = models.CharField(max_length=97, choices=Currency, default='USD')

    class Meta:
        verbose_name_plural = "Profiles"
    

class Beneficiary_Security_Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    beneficiary_legal_name = models.CharField(('ben_legal_name'), max_length=30, blank=True)
    nok_address = models.CharField(('next of kin address'), max_length=300, blank=True)
    nok_relationship = models.CharField(max_length=37, choices=nok_relationship, default='none')
    nok_age = models.CharField(max_length=37, choices=nok_Age, default='none')
    
    employment_type = models.CharField(max_length=37, choices=Employment, default='none')
    salary_range = models.CharField(max_length=37, choices=Salary, default='none')
    
    sq1_select = models.CharField(max_length=37, choices=Security_Question_One, default='none')
    sq2_select = models.CharField(max_length=50, choices=Security_Question_Two, default='none')
    
    sq1_answer = models.CharField(('answer to security question 1'), max_length=300, blank=True)
    sq2_answer = models.CharField(('answer to security question 2'), max_length=300, blank=True)


class AccountDetails(models.Model):
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=12, unique=True)
    routing_number = models.CharField(max_length=9)
    recipient_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.recipient_name} - {self.bank_name}"


class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    txnId = models.UUIDField(default=uuid.uuid4, editable=False)
    txnType = models.CharField(max_length=10,default="Credit", editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=Status, default='Successful')
    date = models.DateTimeField(default=now)

    def __str__(self):
            return f'Deposit details {self.txnId}'
    @property
    def formatted_balance(self):
        '''
        Returns the balance formatted with commas and two decimal places.
        '''
        return f"{self.amount:,.2f}"
    


class Transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    txnId = models.UUIDField(default=uuid.uuid4, editable=False)
    txnType = models.CharField(max_length=10,default="Debit", editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bank_name = models.CharField(max_length=30, null=True)
    action = models.CharField(max_length=30,null=True)
    routing_number = models.CharField(max_length=30,null=True)
    account_number = models.CharField(max_length=30,null=True)
    account_holder = models.CharField(max_length=60,null=True)
    status = models.CharField(max_length=50, choices=Status, default='Successful')
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'Transfer details {self.txnId}'

    @property
    def formatted_amount(self):
        try:
            formatted = f"{self.amount:,.2f}"
            return formatted
        except (ValueError, TypeError):
            return self.amount
        

def get_expiration_time():  
    return now() + timedelta(minutes=5)  
class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)  

    def is_valid(self):
        """Check if the code is still valid."""
        return now() < self.expires_at

    def __str__(self):
        return f'Verification Code for {self.user.username}'

    

class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dep = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name="deposits")
    trans = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name="transfers")
    bal = models.IntegerField()

    @property
    def formatted_balance(self):
        '''
        Returns the balance formatted with commas and two decimal places.
        '''
        return f"{self.bal:,.2f}"

