from django.urls import path
from .views import *
 
urlpatterns = [
    path('', indexPageView, name='dashboard-index'),
    path('register/', registerPageView, name='dashboard-register'),
    path('input/', inputPageView, name='dashboard-input'),
    path("login/", loginPageView, name="dashboard-login"),
    path("logout", logoutPageView, name= "dashboard-logout"),
]
