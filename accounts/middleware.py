# middleware.py
from django.shortcuts import render
from django.contrib.auth import logout

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_blocked:
            logout(request)  # Ensure the user is logged out
            return render(request, "account_templates/account_blocked.html", {
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "formatted_balance": request.user.formatted_balance,
                "date_flagged": request.user.date_flagged,
            })
        return self.get_response(request)
