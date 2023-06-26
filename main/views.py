from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import User, Handle, Contest, Domain, Points
import json
from datetime import datetime
import time
from urllib.request import urlopen, Request
import requests

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else :
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username).first()
            if user:
                print("**")
                user = authenticate(request, username=username, password=password)
                if user is None:
                    messages.error(request, 'Incorrect Password')
                    return redirect('login')
                else:
                    auth_login(request, user)
                    messages.success(request,'Successfuly logged in')
                    return redirect('profile')
            else:
                messages.error(request, "Username is not Correct")
        return render(request, 'main/login.html')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        name = request.POST.get('name')
        user = User.objects.filter(username=username).first()
        if user:
            messages.error(request, "Please choose a different Username")
        elif User.objects.filter(email=email).first():
            messages.error(request, "User Already Exists")
        else:
            password = request.POST.get('password')
            User.objects.create_user(
               name=name, email=email, password=password, username=username)
            messages.success(request,'User Successfuly Created')
            return redirect('login')
    return render(request, 'main/register.html')


@login_required(login_url='login')
def profile(request):
    user = request.user
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            contest = Contest.objects.filter(hostingSite=url).first()
            user = request.user
            user.contest_history.add(contest)
            user.save()
            return redirect(url)
        codeforces_handle = request.POST.get('codeforces_handle')
        lichess_handle = request.POST.get('lichess_handle')
        if codeforces_handle:
            if Handle.objects.filter(handleName=codeforces_handle).first():
                messages.error(request, "Handle already registered with us")
            else:
                domain = Domain.objects.filter(
                    name='https://codeforces.com/').first()
                try:
                    response = requests.get(f'https://codeforces.com/api/user.info?handles={codeforces_handle}')
                    if response.status_code == 200:
                        handle = Handle(handle_domain=domain,
                                        handleName=codeforces_handle, user=user)
                        handle.save()
                except:
                    messages.error(request, "User Handle Not Found")
        if lichess_handle:
            if Handle.objects.filter(handleName=lichess_handle).first():
                messages.error(request, "Handle already registered with us")
            else:
                domain = Domain.objects.filter(
                    name='https://lichess.org/').first()
                try:
                    response = requests.get(f'https://lichess.org/api/user/{lichess_handle}')
                    if response.status_code == 200:
                        handle = Handle(handle_domain=domain,
                                        handleName=lichess_handle, user=user)
                        handle.save()
                except:
                    messages.error(request, "User Handle Not Found")
                # response = requests.get(f'https://lichess.org/api/user/{lichess_handle}')
                # if response.status_code == 200:
                #     handle = Handle(handle_domain=domain,
                #                     handleName=lichess_handle, user=user)
                #     handle.save()
                # else:
                #     print('s')
                #     messages.error(request, "User Handle Not Found")
                print(lichess_handle)
           

    response = {'user': user, 'codeforces': 0, 'codeforces_history': False,
                'lichess': False, 'lichess_history': False, 'upcoming': False}
    for handle in Handle.objects.filter(user=user):
        if str(handle.handle_domain) == 'https://codeforces.com/':
            response.update({'codeforces': requests.get(
                f'https://codeforces.com/api/user.info?handles={handle.handleName}').json()['result'][0]})
            history = user.contest_history.filter(finished=True)
            response.update({'codeforces_history': history})
            contests = Contest.objects.filter(
                finished=False).order_by('timing')
            response.update({'upcoming': contests})
    return render(request, 'main/profile.html', response)


@login_required(login_url='login')
def coupon_page(request):
    if request.method == 'POST':
        cost = int(request.POST.get('coupon'))
        if int(request.user.user_points) >= cost:
            request.user.user_points -= cost
            request.user.save()
            messages.success(request, "Successful")
        else:
            messages.error(request, "You don't have enough points")
    points = request.user.user_points
    return render(request, 'main/coupon.html', {'points': points})


@login_required(login_url='login')
def leaderboard(request, id):
    url = f'https://codeforces.com/contestRegistration/{id}'
    table = Points.objects.filter(
        contest__hostingSite=url)
    leaderboard = table.order_by('score')
    point_table = [35, 15, 15, 5, 5, 5, 5, 5, 5, 5]
    for i, mem in enumerate(leaderboard):
        if not mem.alloted:
            if i > 9:
                point = 1
            else:
                point = point_table[i]
            mem.user.user_points += point
            mem.alloted = True
            mem.save()
            mem.user.save()
    return render(request, 'main/leaderboard.html', {'lead': leaderboard})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    # return redirect('register')

def add_contest(request):
    return None
