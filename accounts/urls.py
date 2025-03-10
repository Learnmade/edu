from django.urls import path
from .views import *
urlpatterns=[
    path('', Home, name="home"),
    path('register/', RegisterView, name="register"),
    path('login/', LoginView, name="login"),
    path('logout/', LogoutView, name="logout"),
    path('forget-password/', ForgetPassword, name="forget-password"),
    path('password-reset-send/<str:reset_id>/', PasswordResetSend, name="password-reset-send"),
    path('reset-password/<str:reset_id>/', ResetPassword, name="reset-password"),
]