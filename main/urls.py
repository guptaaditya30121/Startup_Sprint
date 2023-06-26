from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('leaderboard/<int:id>/', views.leaderboard, name="leaderboard"),
    path('coupon/', views.coupon_page, name="coupon_page"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    
    # path('/reset_password/',
    #      auth_views.PasswordResetView.as_view(),
    #      name="reset_password"),
    
    # path('reset_password_sent/', 
    #      auth_views.PasswordResetDoneView.as_view(), 
    #      name="password_reset_done"),
    
    
    # path('reset/<uibd64>/<token>/', 
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name="password_reset_confirm") , #user id encoded in base64
    
    
    # path('reset_password_complete/', 
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name="password_reset_complete")
    
]
