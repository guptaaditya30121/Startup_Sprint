from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path('leaderboard/<int:id>', views.leaderboard, name="leaderboard"),
    path('coupon', views.coupon_page, name="coupon_page")
]
