from accounts.models import Profile
from django.utils import timezone

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_profile, created = Profile.objects.get_or_create(user=request.user) 
            user_profile.browser = request.META.get('HTTP_USER_AGENT')
            user_profile.ip_address = request.META.get('REMOTE_ADDR')
            user_profile.login_time = timezone.now()
            user_profile.save()

        response = self.get_response(request)
        return response    