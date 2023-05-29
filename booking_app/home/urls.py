from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_page, name="login page"),
    path('register/', register_page, name="register page"),
]