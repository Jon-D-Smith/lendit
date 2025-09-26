from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm, CustomUserChangeForm


def bootstrap_class_error_handling(form):
    for field in form.errors:
        form.fields[field].widget.attrs['class'] += ' is-invalid'

# Route to setup a super user when the application is first launched as a new/clean instance
def setup_superuser(request):
    User = get_user_model()

    # Seeing if a user has already been created. If so, redirect to the normal registration form. We only want one superuser by default.
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
            messages.success(request, 'Administrative account created successfully!')
            return redirect('admin:index')
        else:
            # Kind of clunky but it works for validation errors with bootstrap
            bootstrap_class_error_handling(form)
            return render(request, 'accounts/setup_superuser.html', {'form':form})
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/setup_superuser.html', {'form':form})


def register(request):
    User = get_user_model()
    # If this is the first user, redirect to setup superuser
    if User.objects.count() == 0:
        return redirect('accounts:setup_superuser')
    
    # If logged in, redirect to home page. Why are we trying to login again?!?
    if request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account registered successfully')
            return redirect('accounts:login')
        else:
            bootstrap_class_error_handling(form)
            return render(request, 'accounts/register.html', {'form':form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form':form})



def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('accounts:login')
        else:
            bootstrap_class_error_handling(form)
            return render(request, 'accounts/login.html', {'form':form}) 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

# This is our most complicated view. 
def logout_user(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('accounts:login')

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Profile successfully updated')
            return redirect('accounts:edit_user')
        else:
            bootstrap_class_error_handling(form)
            return render(request, 'accounts/edit_profile.html', {'form': form})
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form':form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in by updating the session
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed!')
            return redirect('accounts:login')
        else:
            bootstrap_class_error_handling(form)
            return render(request, 'accounts/change_password.html', {'form':form})
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
