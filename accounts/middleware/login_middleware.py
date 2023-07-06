from django.shortcuts import redirect,reverse

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        
        login_required_urls = [
                'admin-all-users',
                'admin-user-create',
                'admin-user-edit',
                'admin-user-delete',
                
                'admin-all-category',
                'admin-category-create',
                'admin-category-edit',
                'admin-category-delete',
                
                'admin-product-create',
                'admin-all-product',
                'admin-product-edit',
                'admin-product-delete',
                
                'admin-product-variant-add',
                'admin-product-variant-edit',
                'admin-product-variant-delete',
                
                'admin-all-brand',
                'admin-brand-create',
                
                'admin-all-atribute',
                'admin-atribute-create',
                
                'admin-all-atribute_value',
                'admin-atribute_value-create',
                
                
                'admin-all-orders',
                'admin-order-history-detail',
                'change_order_status_admin',
                
                #add login required for admin urls name  , here     
                
            ]
        if request.resolver_match and request.resolver_match.url_name in login_required_urls and not (request.user.is_authenticated and request.user.is_staff):
            return redirect('admin-login')
            
        return response