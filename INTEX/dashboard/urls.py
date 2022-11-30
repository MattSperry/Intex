from django.urls import path
from .views import loginPageView, indexPageView, registerPageView, inputPageView, profilePageView, updateInfoView, logoutPageView, journalPageView, suggestionsPageView, journalEntryAdd, foodSearch, updateDataView, addFoodItem, addFoodItemEntry
 
urlpatterns = [
    path("", loginPageView, name="dashboard-login"),
    path("index/", indexPageView, name="dashboard-index"),
    path("register/", registerPageView, name="dashboard-register"),
    path("input/", inputPageView, name="dashboard-input"),
    path("profile/", profilePageView, name="dashboard-profile"),
    path("update/", updateInfoView, name="dashboard-update"),
    path("logout/", logoutPageView, name= "dashboard-logout"),
    path("journal/", journalPageView, name="dashboard-journal"),
    path("suggestions/", suggestionsPageView, name="dashboard-suggestions"),
    path('addJournalEntry/', journalEntryAdd, name='journalEntryAdd'),
    path('foodSearch/', foodSearch, name='foodSearch'),
    path("updatePerson/", updateDataView, name='update-person-info'),
    path("addFoodItem/", addFoodItem, name='addFoodItem'),
    path('addFoodItemEntry/', addFoodItemEntry, name='addFoodItemEntry')
]
