from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.conf import settings
from .models import User
from .getDetails import UserData
import requests
import json

# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, 'Incorrect Password')
            else:
                auth_login(request, user)
                return redirect('profile')
        else:
            messages.error(request, "Username is not Correct")
    return render(request, 'main/login.html')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(
            email=email, password=password, username=username)
        return redirect('login')
    return render(request, 'main/register.html')


@login_required(login_url='login')
def profile(request):
    user = request.user
    response = {'user': user, 'codeforces': 0,
                'lichess': False}
    for handle in user.handles.all():
        if str(handle.handle_domain) == 'https://codeforces.com/':
            response.update({'codeforces': UserData(
                handle.handleName).get_details('codeforces')})
    # response.update({'codeforces_history': requests.get(
    #     f'https://codeforces.com/api/user.info?handles={handle.handleName}').json()['result'][0]})
        if str(handle.handle_domain) == 'https://lichess.org/':
            response.update({'lichess': requests.get(
                f'https://lichess.org/api/user/{handle.handleName}').json()})
            resp = requests.get(
                f'https://lichess.org/api/games/user/{handle.handleName}?max=10', headers={'Accept': 'application/x-ndjson'})
            list_resp = resp.text.splitlines()
            json_resp = list(map(lambda x: json.loads(x), list_resp))
            response.update({'lichess_history': json_resp})

    print(response)
    return render(request, 'main/profile.html', response)

def leaderboard(request):
    return render(request , 'main/leaderboard.html')

def coupon_page(request):
    return render(request, 'main/coupon.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
