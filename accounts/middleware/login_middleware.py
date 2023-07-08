from django.shortcuts import redirect,reverse

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
      
        excluded_urls = [
            'admin-login',
            'admin-login-otp',
            'admin-login-otp-verify'
            # Add other excluded URL names here
        ]
        
        
        if '/admincontrol' in request.path and request.resolver_match and request.resolver_match.url_name not in excluded_urls:
            if not (request.user.is_authenticated and request.user.is_staff):
                return redirect('admin-login')
            
        return response