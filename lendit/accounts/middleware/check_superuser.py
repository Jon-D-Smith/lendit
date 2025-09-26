from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

class CheckSuperuserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        User = get_user_model()
        user_count = User.objects.count()

        setup_path = reverse('accounts:setup_superuser')

        if request.path == setup_path or request.path.startswith('/static') or request.path.startswith('/admin'):
            return None
        
        if user_count == 0:
            return redirect(setup_path)
        
        return None