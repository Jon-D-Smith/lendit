from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('setup/', views.setup_superuser, name='setup_superuser'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_user/', views.edit_user, name='edit_user'),
]
