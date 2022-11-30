from django.shortcuts import render, redirect
from .models import Person, JournalEntry, Comorbidity, Race, Food
from .forms import UserForm, PersonForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import requests
 
 
# Create your views here.
def registerPageView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            customer = form.save()
            login(request, customer)
            messages.success(request, "Registration Successful.")
            return redirect("dashboard-input")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserForm()
    return render (request=request, template_name="dashboard/register.html", context={"register_form":form})

def inputPageView(request):
    data = Person.objects.all()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard-index")
    else:
        form = PersonForm()
    context = {
        'data': data,
        'form': form,
    }
    return render(request, "dashboard/input.html", context)

def profilePageView(request):
    context = {
        "info" : Person.objects.get(personID  = request.user.id)
    }
    return render(request, "dashboard/profile.html", context)

def updateInfoView(request):

    context = {
        "info" : Person.objects.get(personID  = request.user.id),
        'comorbidities' : Comorbidity.objects.all(),
        "races" : Race.objects.all()
    }
    return render(request, "dashboard/update.html", context)

def updateDataView(request):
    if request.method == "POST":
        person = Person.objects.get(personID=request.user.id)

        person.first_name = request.POST["first_name"]
        person.last_name = request.POST["last_name"]
        person.comorbidity = Comorbidity.objects.get(name = request.POST["comorbidity"])
        person.date_of_birth = request.POST["date_of_birth"]
        person.weight = request.POST["weight"]
        person.height = request.POST["height"]
        person.gender = request.POST["gender"]
        person.race = Race.objects.get(race = request.POST["race"])
        
        person.save()
    return updateInfoView(request)

def loginPageView(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("dashboard-index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="dashboard/login.html", context={"login_form":form})

def logoutPageView(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("dashboard-login")

def journalPageView(request):
    data = Person.objects.all()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PersonForm()
    context = {
        'data': data,
        'form': form,
    }
    return render(request, 'dashboard/journal.html', context)

def suggestionsPageView(request):
    return render(request, 'dashboard/suggestions.html')

def indexPageView(request):
    context = {
        'currentUser': Person.objects.get(personID  = request.user.id)
    }
    return render(request, 'dashboard/index.html', context)

def journalEntryAdd(request):
    if request.method == 'POST':
        new_entry = JournalEntry()
        person = Person.objects.get(personID = request.user.id)
        new_entry.personID = person.personID
        new_entry.date_time_eaten = request.POST['dateTime']
        new_entry.food_name = request.POST['food_name']
        new_entry.amount = request.POST['amount']
        new_entry.save()

        """new_food = Food()

        new_food.food_name = request.POST['food_name']

        query = request.POST['food_name']
        dataType = 'Foundation'
        pageSize = 10
        pageNumber = 1
        api_key = 'F92KbXwQwUXrteSO6PpQ7zocfxkkrt5inVeLVwqI'

        url = "https://api.nal.usda.gov/fdc/v1/foods/search?query=" + query + "&dataType=" + dataType + "&pageSize=" + str(pageSize) + "&pageNumber=" + str(pageNumber) + "&api_key=" + api_key


        payload={}
        headers = {
        'Cookie': 'ApplicationGatewayAffinity=5164bd01bfd5c519ce1bd2870a3ce176; ApplicationGatewayAffinityCORS=5164bd01bfd5c519ce1bd2870a3ce176'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()

        new_food.serving_size = 
        new_food.units = request.POST['units']
        new_food.potassium = request.POST['potassium']
        new_food.phosphorus = request.POST['phosphorus']
        new_food.sodium = request.POST['sodium']
        new_food.calcium = request.POST['calcium']
        new_food.protein = request.POST['protein']
        new_food.sugar = request.POST['sugar']

        new_food.save()"""

    return redirect('/index')

def foodSearch(request):

    query = request.POST['search']
    dataType = 'Foundation'
    pageSize = 10
    pageNumber = 1
    api_key = 'F92KbXwQwUXrteSO6PpQ7zocfxkkrt5inVeLVwqI'

    url = "https://api.nal.usda.gov/fdc/v1/foods/search?query=" + query + "&dataType=" + dataType + "&pageSize=" + str(pageSize) + "&pageNumber=" + str(pageNumber) + "&api_key=" + api_key


    payload={}
    headers = {
    'Cookie': 'ApplicationGatewayAffinity=5164bd01bfd5c519ce1bd2870a3ce176; ApplicationGatewayAffinityCORS=5164bd01bfd5c519ce1bd2870a3ce176'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()

    food_array = []
    for food in json_response['foods']:
        food_array.append(food['description'])


    context = {
        'food_names' : food_array
    }

    return render(request, 'dashboard/journal.html', context)

def addFoodItem(request):
    return render(request, 'dashboard/addFood.html')

def addFoodItemEntry(request):
    if request.method == 'POST':
        new_food = Food()

        new_food.food_name = request.POST['food_name']
        new_food.serving_size = request.POST['serving_size']
        new_food.units = request.POST['units']
        new_food.potassium = request.POST['potassium']
        new_food.phosphorus = request.POST['phosphorus']
        new_food.sodium = request.POST['sodium']
        new_food.calcium = request.POST['calcium']
        new_food.protein = request.POST['protein']
        new_food.sugar = request.POST['sugar']

        new_food.save()

    return render(request, 'dashboard/journal.html')


    




    

