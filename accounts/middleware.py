# middleware.py
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_blocked:
            logout(request)
            return redirect(reverse('account_blocked'))
        return self.get_response(request)
