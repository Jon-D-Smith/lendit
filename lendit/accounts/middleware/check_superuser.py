from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class CheckSuperuserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = get_user_model()
        user_count = user.objects.count()

        setup_path = reverse("accounts:setup_superuser")

        # No need to redirect if any of these cases are found
        if (
            request.path == setup_path
            or request.path.startswith("/static")
            or request.path.startswith("/admin")
        ):
            return None

        # If we have no users, prompt superuser setup
        if user_count == 0:
            return redirect(setup_path)

        return None
