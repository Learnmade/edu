from django.urls import path
from . import views
urlpatterns=[
    path('home/', views.home, name="home"),
    path('register/',views.register_user, name="register"),
    path('login/', views.login_user, name="login")
]