from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from .forms import ProfileCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Keyword
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie


def create_profile(request):
    """
    Handles user signup at /accounts/signup/
    """
    if request.method == 'POST':
        # form was submitted
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password1']
            profile = authenticate(email=email, password=password)
            login(request, profile)
            return redirect('home')

        # if invalid, render form with errors generated by Django
        return render(request, 'registration/signup.html', {'form': form})

    else:
        # form has not been submitted yet
        # check if user is authenticated
        if request.user.is_authenticated:
            return redirect('account')

        # render blank form
        form = ProfileCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


def login_profile(request):
    """
    Handles user login at /accounts/login
    """
    if request.method == 'POST':
        # form was submitted
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('account')

        # if invalid, render form with errors generated by Django
        return render(request, 'registration/login.html', {'form': form})

    else:
        # form has not been submitted yet
        # if user is already logged in, redirect to their account home page
        if request.user.is_authenticated:
            return redirect('account')

        # render blank form
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_profile(request):
    """
    Logs out the user and redirects to the website landing page
    """
    logout(request)
    return redirect('/')


@login_required
@ensure_csrf_cookie
def account(request):
    # profile = Profile.objects.get(email=request.user.email)
    # email = profile.email
    # phone = profile.phone
    #
    # context = {}

    # Gather all keywords associated with user using a QuerySet
    # keywords = Keyword.objects.filter(user__email__exact=email)
    # context['keywords'] = keywords
    # context['email'] = email
    # context['phone'] = phone

    return render(request, 'home.html')  # context


def load_keywords(request):
    profile = Profile.objects.get(email=request.user.email)
    keywords = Keyword.objects.filter(user__email__exact=profile.email)
    data = []
    for obj in keywords:
        item = {
            'id': obj.id,
            'user': obj.user.id,
            'keyword': obj.keyword
        }
        data.append(item)
    return JsonResponse({'data': data})


def delete_keyword(request):
    if request.method == 'POST':
        keyword_to_delete = Keyword.objects.get(pk=request.POST['keyword_id'])
        data = {'data': keyword_to_delete.delete()}
        return JsonResponse(data)
    else:
        return redirect('account')

