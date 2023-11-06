# Create your models here.
from __future__ import unicode_literals
import uuid
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .country import Currency

from django.contrib.auth.base_user import BaseUserManager


Title = (
    ('none', 'Please Select Title'),
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'),
    ('Mr&Mrs.', 'Mr&Mrs.'),
    ('Ms.', 'Ms.'),
    ('Miss.', 'Miss.'),
)

Gender = (
    ('none', 'Please Select Gender'),
    ('Male', 'Male'),
    ('Female', 'FeMale'),
    ('Other', 'Other')
)


Account_Type = (
    ('none','Please select Account Type'),
    ('Checking Account', 'Checking Account'),
    ('Savings Account', 'Savings Account'),
    ('Fixed Deposit Account', 'Fixed Deposit Account'),
    ('Current Account','Current Account'),
    ('Business Account', 'Business Account'),
    ('Non Resident Account','Non Resident Account'),
    ('Cooperate Business Account', 'Cooperate Business Account'),
    ('Investment Account', 'Investment Account'),
)


# custom user and manager area
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
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

        
        

        if extra_fields.get('is_superuser', 'is_staff') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class Country(models.Model):
    # id = models.AutoField()
    name = models.CharField(('country name'), max_length=55, blank=True)

    def __str__(self):
        return self.name
    

class State(models.Model):
    name = models.CharField(('state name'), max_length=55, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('middle name'), max_length=30, blank=True)
    
    middle_name = models.CharField(('last name'), max_length=30, blank=True)
    nick_name = models.CharField(('nick name'), max_length=30, blank=True)
    date_of_birth = models.DateField(('date of birth'), max_length=30, blank=True)
    zip_code = models.PositiveIntegerField(('zip code'))
    residential_address = models.CharField(('residential address'), max_length=300, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    State = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(('city'),max_length=55, blank=True)
    ssn = models.CharField(('ssn'), max_length=30, blank=True)
    phone_number = models.CharField(('phone number'), max_length=30, blank=True)
    
    title = models.CharField(max_length=17, choices=Title, default='none')
    gender = models.CharField(max_length=17, choices=Gender, default='none')
    account_type = models.CharField(max_length=37, choices=Account_Type, default='none')
    Currency_type = models.CharField(max_length=97, choices=Currency, default='USD')
    
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    account_number = models.IntegerField(('account_number'), unique=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        User.objects.filter(pk=instance.id).update(account_number=int(str(uuid.uuid4().int)[:10]))
        

# @receiver(post_save, sender=User)
# def save_author(sender, instance, **kwargs):
#     instance.User.save()



#  bank model area


class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    txnId = models.UUIDField(default=uuid.uuid4, editable=False)
    txnType = models.CharField(max_length=10,default="Credit", editable=False)
    amount = models.CharField(max_length=30)
    action = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f'Deposit details {self.Deposit.txnId}'


class Transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    txnId = models.UUIDField(default=uuid.uuid4, editable=False)
    txnType = models.CharField(max_length=10,default="Debit", editable=False)
    amount = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f'Transfer details  {self.Transfer.txnId}'



class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dep = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name="deposits")
    trans = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name="transfers")
    bal = models.IntegerField()

# @receiver(post_save, sender=Book)
# def create_author(sender, instance, created, **kwargs):
#     if created:
#         author = Author.objects.create(id=your_id,author_name=your_author_name,author_description=your_author_description)
#         Book.objects.objects.filter(pk=instance.id).update(author=author)


# @receiver(post_save, sender=Book)
# def save_author(sender, instance, **kwargs):
#     instance.author.save()
