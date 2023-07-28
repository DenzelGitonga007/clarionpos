from django.shortcuts import render, redirect
from  .forms import UserRegistrationForm, LoginForm
# To display message
from django.contrib import messages
# For authentication
from django.contrib.auth.decorators import login_required # only super admin can create the user-- has to log in
from django.contrib.admin.views.decorators import staff_member_required # only super admin can create the user
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# Home view
def home(request):
    return render(request, 'accounts/home.html', context={})


# Creating the user
@staff_member_required(login_url='accounts:login')
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Congratulations! You have created an account successfully! Now login below...")
            return redirect('accounts:login') # the login url pattern
        # If error in creation
        else:
            messages.error(request, 'There was an error while creating your account. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # If user exist
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    # Success message
                    messages.success(request, "Welcome Admin... You have logged in successfully!")
                    # Redirect super admin to the dashboard
                    return redirect('admin_dashboard:dashboard')
                else:
                    # Success message
                    messages.success(request, "Congratulations! You have logged in successfully!")
                    # Redirect new users to the home page
                    return redirect('accounts:home')
                    
                # # Redirect them
                # return redirect('accounts:home')
            # else:
            #     # Error message if credentials are wrong
            #     form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout
def logout_user(request):
    logout(request)
    # Success message
    messages.success(request, "We hope we have been of use to you...")
    return render(request, 'accounts/logout.html')