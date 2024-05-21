from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .forms import ProfileCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.contrib import messages


# Create your views here.
def create_profile(request):
    context = {'form': ProfileCreationForm()}

    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email'].lower()
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password1']
            # profile = Profile.objects.create_user(email, password, {'phone': phone})
            profile = authenticate(email=email, password=password)
            login(request, profile)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        # check if user is authenticated
        # if so, log out user then display this page
        if request.user.is_authenticated:
            return HttpResponse(f"You are already authenticated as {request.user.email}")

        # context['form'] = ProfileCreationForm()

    return render(request, 'registration/signup.html', context)


def login_profile(request):
    # context = {'form': AuthenticationForm()}

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('account')

        return render(request, 'registration/login.html', {'form': form})

    else:
        form = AuthenticationForm()

        return render(request, 'registration/login.html', {'form': form})


def logout_profile(request):
    logout(request)
    return redirect('/')


def account(request):
    return HttpResponse("Account home")
