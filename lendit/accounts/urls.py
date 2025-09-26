from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('setup/', views.setup_superuser, name='setup_superuser'),
    path('register/', views.register, name='register'),
]
