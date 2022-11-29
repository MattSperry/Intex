from django.urls import path
from .views import *
 
urlpatterns = [
    path("", loginPageView, name="dashboard-login"),
    path("index/", indexPageView, name="dashboard-index"),
    path("register/", registerPageView, name="dashboard-register"),
    path("input/", inputPageView, name="dashboard-input"),
    path("logout", logoutPageView, name= "dashboard-logout"),
    path("journal/", journalPageView, name="dashboard-journal"),
    path("suggestions/", suggestionsPageView, name="dashboard-suggestions"),
    ]
