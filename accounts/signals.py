# from django.db.models.signals import post_save  
# from django.dispatch import receiver  
# from django.core.mail import send_mail  
# from django.conf import settings  
# from .models import User 
# from .utils import send_welcome_email

# @receiver(post_save, sender=User)  
# def send_welcome_email(sender, instance, created, **kwargs):  
#     if created:  # Check if it's a new user  
#         subject = 'Welcome to Our Capital Funding Financial Online Banking Website'  
#         message = f"""  
#         Dear {instance.first_name},  

#         Thank you for signing up with us!  
#         Your account has been successfully created. Below are your account details:  
#         Account Number: {instance.account_number}  
#         Email: {instance.email}  
#         Balance: {instance.bal}

#         Please log in to your account, make deposit, manage your finances, and pay bills.

#         Best regards,  
#         The Banking Team  
#         """  
#         recipient_email = instance.email  
#         send_mail(  
#             subject,  
#             message,  
#             settings.DEFAULT_FROM_EMAIL,  
#             [recipient_email],  
#             fail_silently=False,  
#         )

# @receiver(post_save, sender=User)
# def user_created_handler(sender, instance, created, **kwargs):
#     """Sends a welcome email when a new user is created."""
#     if created:
#         send_welcome_email(instance)