from django.urls import path
from .views import *
 
urlpatterns = [
    path("", loginPageView, name="dashboard-login"),
    path("index/", indexPageView, name="dashboard-index"),
    path("register/", registerPageView, name="dashboard-register"),
    path("<id>input/", inputPageView, name="dashboard-input"),
    path("<id>update/", updateInfoView, name="dashboard-update"),
    path("logout", logoutPageView, name= "dashboard-logout"),
    path("journal/", journalPageView, name="dashboard-journal"),
    path("suggestions/", suggestionsPageView, name="dashboard-suggestions"),
    path('addJournalEntry/', journalEntryAdd, name='journalEntryAdd'),
    ]
