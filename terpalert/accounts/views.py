from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from .forms import ProfileCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Alert, Menu, DailyMenu
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Case, Value, When, CharField
from datetime import date


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
            return redirect('account')

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
    """
    Renders the account page
    Login is required, otherwise user will be redirected to the login page
    Context includes alert notifications for user
    """
    context = {'notifications': False, 'data': [], 'date': date.today()}

    # Find today's alerts (if any) for user
    alerts = Alert.objects.filter(user__email__exact=request.user.email).order_by('menu_item')
    for alert in alerts:  # All the user's alerts
        daily_menu_item = DailyMenu.objects.filter(menu_item_id=alert.menu_item.id, date=date.today())

        if daily_menu_item.exists():  # Alert is in the daily menu for today's date
            context['notifications'] = True

            # Add dining halls the alert is applicable to
            dining_halls = []
            if daily_menu_item[0].yahentamitsi_dining_hall:
                dining_halls.append('Yahentamitsi')
            if daily_menu_item[0].south_dining_hall:
                dining_halls.append('South')
            if daily_menu_item[0].two_fifty_one_dining_hall:
                dining_halls.append('251')

            context['data'].append([alert.menu_item.item, ', '.join(dining_halls)])

    return render(request, 'home.html', context)


@login_required
def load_alerts(request):
    """
    Handle the Ajax request to retrieve the alerts for the current user
    All alerts for that user are returned in order of date created, most recent first

    :return: JsonResponse containing a list with fields "id" and "alert"
    """
    alerts = Alert.objects.filter(user__email__exact=request.user.email).order_by('-date_created', 'id')
    data = []
    for alert in alerts:
        item = {
            'id': alert.id,
            'alert': alert.menu_item.item,
        }
        data.append(item)
    return JsonResponse({'data': data})


def delete_alert(request):
    """
    Deletes the alert given by Ajax request

    :return: JsonResponse containing the deleted object
    """
    if request.method == 'POST':
        alert_to_delete = Alert.objects.get(pk=request.POST['alert-id'])
        data = {'data': alert_to_delete.delete()}
        return JsonResponse(data)
    else:
        return redirect('home')  # Redirect any attempts to access this page


def save_alert(request):
    """
    Saves the alert given by Ajax request
    Alert won't save if the alert isn't a Menu item or if it is already an alert for the user

    :return: JsonResponse containing the alert and its id. If saving was unsuccessful, message is returned
    """
    if request.method == 'POST':
        alert_item = request.POST['alert']
        data = {}

        try:
            menu_item = Menu.objects.get(item=alert_item)
        except Menu.DoesNotExist:
            data['success'] = False
            data['message'] = 'This menu item does not exist!'
        else:
            # Check if alert already exists for the user
            if Alert.objects.filter(menu_item_id=menu_item.id, user_id=request.user.id).exists():
                data['success'] = False
                data['message'] = 'This alert has already been added!'

            else:
                saved_alert = Alert.objects.create(menu_item_id=menu_item.id, user_id=request.user.id)

                if saved_alert is not None:
                    # Database operation was successful
                    data['success'] = True
                    data['id'] = saved_alert.id
                    data['alert'] = alert_item
                else:
                    # Something went wrong with create()
                    data['success'] = False
                    data['message'] = 'Something went wrong with saving this alert'
        finally:
            return JsonResponse(data)
    else:
        return redirect('account')  # Redirect any attempts to access this page


def load_menu(request):
    """
    Handle the Ajax request to retrieve search results for autocomplete
    Results are ordered starting with ones starting with the search term,
    followed by ones containing the term in alphabetical order

    :return: JsonResponse containing a list with fields "label" and "value"
    """
    if 'term' in request.GET:
        term = request.GET['term']
        menu = Menu.objects.annotate(
            order_by_position=Case(
                When(item__istartswith=term, then=Value(1)),
                When(item__icontains=term, then=Value(2)),
                default=Value(3),
                output_field=CharField(),
            )
        ).filter(item__icontains=term).order_by('order_by_position', 'item')
        data = []
        for item in menu:
            item = {
                'label': item.item,
                'value': item.id,
            }
            data.append(item)

        return JsonResponse({'data': data})
    else:
        return redirect('account')
