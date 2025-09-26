from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model

from .forms import CustomUserCreationForm


# Create your views here.

def setup_superuser(request):
    User = get_user_model()

    if User.objects.count() > 0:
        return redirect('accounts:register')
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
            )
            login(request, user)
            return redirect('admin:index')
        else:
            for field in form.errors:
                form.fields[field].widget.attrs['class'] += ' is-invalid'
            return render(request, 'accounts/setup_superuser.html', {'form':form})
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/setup_superuser.html', {'form':form})


def register(request):
    User = get_user_model()
    if User.objects.count() == 0:
        return redirect('accounts:setup_superuser')
    
    if request.user.is_authenticated:
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin:index')
        else:
            for field in form.errors:
                form.fields[field].widget.attrs['class'] += ' is-invalid'
            return render(request, 'accounts/register.html', {'form':form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form':form})