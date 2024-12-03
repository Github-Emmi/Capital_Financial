from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def get_full_url(path):
    """Helper function to generate a full URL from a path."""
    return f"{settings.SITE_URL.rstrip('/')}/{path.lstrip('/')}"

def send_welcome_email(user):
    """Sends a welcome email with a verification link."""
    subject = "Activate Your Capital Financial Account Email"
    
    # Generate activation link
    activation_path = reverse('verify_email', kwargs={
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    activation_url = get_full_url(activation_path)

    # Prepare email context
    context = {
        'user': user,
        'activation_url': activation_url,
    }

    # Render HTML and plain text messages
    html_message = render_to_string('account_templates/welcome_email.html', context)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
