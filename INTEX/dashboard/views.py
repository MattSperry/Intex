from django.shortcuts import render, redirect
from .models import Person, JournalEntry, Comorbidity, Race, Food
from .forms import UserForm, PersonForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import requests
from datetime import date, timedelta, datetime
 
# Create your views here.
def registerPageView(request):
    success = True
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            customer = form.save()
            login(request, customer)
            messages.success(request, "Registration Successful.")
            return redirect("dashboard-input")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        success = False
    form = UserForm()
    context={
        "register_form": form,
        "success" : success,
        }
    return render (request, "dashboard/register.html", context)

def inputProcess(request):
    if request.method == "POST":
        person = Person()

        person.personID = User.objects.get(id = request.user.id)
        person.first_name = request.POST["first_name"]
        person.last_name = request.POST["last_name"]
        person.comorbidity = Comorbidity.objects.get(name = request.POST["comorbidity"])
        person.date_of_birth = request.POST["date_of_birth"]
        person.weight = request.POST["weight"]
        person.height = request.POST["height"]
        person.gender = request.POST["gender"].lower().capitalize()
        person.race = Race.objects.get(race = request.POST["race"])
        
        person.save()

        return redirect("dashboard-index")

def inputPageView(request):
    
    context = {
        "comorbidities" : Comorbidity.objects.all(),
        "races" : Race.objects.all()
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
        person.gender = request.POST["gender"].lower().capitalize()
        person.race = Race.objects.get(race = request.POST["race"])
        
        person.save()

        return redirect("dashboard-profile")
    return updateInfoView(request)

def loginPageView(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
            #user = User.objects.get(username = username, password = password)
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
    currentPerson = Person.objects.get(personID  = request.user.id)

    data = JournalEntry.objects.filter(personID = request.user.id, date_recorded = datetime.today())
    potassium = 0
    phosphorus = 0
    sodium = 0
    calcium = 0
    protein = 0
    sugar = 0

    for entry in data:
        food = Food.objects.get(food_name = entry.food_name)
        potassium += food.potassium * entry.amount
        phosphorus += food.phosphorus * entry.amount
        sodium += food.sodium * entry.amount
        calcium += food.calcium * entry.amount
        protein += ((food.protein * entry.amount) * 10)
        sugar += ((food.sugar * entry.amount) * 10)
    
    rprotein = 0
    person = Person.objects.get(personID = request.user.id)
    rprotein = person.weight * 0.45359237 * .6 * 100
        
    rsugar = 0
    if person.gender == 'Male' :
        rsugar = 3600
    else :
        rsugar = 2500
    
    data = [2750, 900, 2702, 2000, rprotein, rsugar]

    alerts = ''
    if potassium > data[0]:
        alerts += 'Potassium '
    if phosphorus > data[1]:
        alerts += 'Phosphorus '
    if sodium > data[2]:
        alerts += 'Sodium '
    if calcium > data[3]:
        alerts += 'Calcium '
    if protein > data[4]:
        alerts += 'Protein '
    if sugar > data[5]:
        alerts += 'Sugar '
     
    potassiumAvoid = None
    phosphorusAvoid = None
    sodiumAvoid = None
    calciumAvoid = None
    proteinAvoid = None
    sugarAvoid = None

    if 'Potassium' in alerts:
        potassiumAvoid = ["Banana", "Spinach", "Beans"]
    if 'Phosphorus' in alerts:
        phosphorusAvoid = ["Chicken", "Nuts", "Fish"]
    if 'Sodium' in alerts:
        sodiumAvoid = ["Cereal", "Cheese", "Pizza"]
    if 'Calcium' in alerts:
        calciumAvoid = ["Milk", "Yogurt", "Cheese"]
    if 'Protein' in alerts:
        proteinAvoid = ["Chicken", "Fish", "Eggs"]
    if 'Sugar' in alerts:
        sugarAvoid = ["Candy", "Soda", "Desserts"]

    if currentPerson.comorbidity.name != None:
        comorbidity = currentPerson.comorbidity.name

    reccomendedFoods = None
    badFoods = None
    if comorbidity == "High Blood Pressure":
        reccomendedFoods = ["Fruits", "Vegetables", "Whole grains", "Low-fat dairy", "Chicken", "Fish", "Nuts"]
        badFoods = ["Sodium", "Red meat", "Candy", "Soda", "Tea", "Saturated fat", "Trans fat"]
    elif comorbidity == "Diabetes type 1":
        reccomendedFoods = ["Fish", "Spinach", "Kale", "Avocados", "Eggs", "Chia seeds", "Oatmeal",
        "Milk", "Cheese", "Beans", "Yogurt (plain)", "Nuts", "Broccoli", "Cauliflower", "Brussel sprouts", 
        "Cabbage", "Quinoa", "Whole grain", "Brown rice", "Flaxseeds", "Olives", "Sweet potatoes", 
        "Strawberries", "Garlic", "Squash", "Fruits", "Berries"]
        badFoods = ["White bread", "Bagels", "Pasta", "Rice", "Soda", "Tea", "Fried foods", "Alcohol",
        "Cereal", "Candy", "Pumpkin", "Processed meats", "Fruit juice", "Melons", "Pineapple", "Popcorn",
        "White potatoes", "Margarine", "Peanut butter", "Trans fat", "Brown sugar", "Honey", "Syrup",
        "Pretzels", "Graham crackers", "Saltines", "French fries"]
    elif comorbidity == "Diabetes type 2":
        reccomendedFoods = ["Fish", "Spinach", "Kale", "Avocados", "Eggs", "Chia seeds", "Oatmeal",
        "Milk", "Cheese", "Beans", "Yogurt (plain)", "Nuts", "Broccoli", "Cauliflower", "Brussel sprouts", 
        "Cabbage", "Quinoa", "Whole grain", "Brown rice", "Flaxseeds", "Olives", "Sweet potatoes", 
        "Strawberries", "Garlic", "Squash", "Fruits", "Berries"]
        badFoods = ["White bread", "Bagels", "Pasta", "Rice", "Soda", "Tea", "Fried foods", "Alcohol",
        "Cereal", "Candy", "Pumpkin", "Processed meats", "Fruit juice", "Melons", "Pineapple", "Popcorn",
        "White potatoes", "Margarine", "Peanut butter", "Trans fat", "Brown sugar", "Honey", "Syrup",
        "Pretzels", "Graham crackers", "Saltines", "French fries"]
        
    context = {
        "recommendedFoods" : reccomendedFoods,
        "badFoods" : badFoods,
        "potassiumAvoid" : potassiumAvoid,
        "phosphorusAvoid" : phosphorusAvoid,
        "sodiumAvoid" : sodiumAvoid,
        "calciumAvoid" : calciumAvoid,
        "proteinAvoid" : proteinAvoid,
        "sugarAvoid" : sugarAvoid,
        "comorbidity" : comorbidity,
    }
    
    return render(request, 'dashboard/suggestions.html', context)

def indexPageView(request):
    data = JournalEntry.objects.filter(personID = request.user.id, date_recorded = datetime.today())
    potassium = 0
    phosphorus = 0
    sodium = 0
    calcium = 0
    protein = 0
    sugar = 0

    for entry in data:
        food = Food.objects.get(food_name = entry.food_name)
        potassium += food.potassium * entry.amount
        phosphorus += food.phosphorus * entry.amount
        sodium += food.sodium * entry.amount
        calcium += food.calcium * entry.amount
        protein += ((food.protein * entry.amount) * 10)
        sugar += ((food.sugar * entry.amount) * 10)
    
    rprotein = 0
    person = Person.objects.get(personID = request.user.id)
    rprotein = person.weight * 0.45359237 * .6 * 100
        
    rwater = 0
    rsugar = 0
    if person.gender == 'Male' :
        rwater = 3700
        rsugar = 3600
    else :
        rwater = 2700
        rsugar = 2500

    week_potassium = []
    week_phosphorus = []
    week_sodium = []
    week_calcium = []
    week_protein = []
    week_sugar = []
    week_potassium.append(potassium)
    week_phosphorus.append(phosphorus)
    week_sodium.append(sodium)
    week_calcium.append(calcium)
    week_protein.append(protein)
    week_sugar.append(sugar)
    
    data = [2750, 900, 2702, 2000, rprotein, rsugar]

    alerts = ''
    if potassium > data[0]:
        alerts += 'Potassium '
    if phosphorus > data[1]:
        alerts += 'Phosphorus '
    if sodium > data[2]:
        alerts += 'Sodium '
    if calcium > data[3]:
        alerts += 'Calcium '
    if protein > data[4]:
        alerts += 'Protein '
    if sugar > data[5]:
        alerts += 'Sugar '

    for i in range(1,7) :
        today = datetime.today()
        new_day = (today - timedelta(days=i))
        day_data = JournalEntry.objects.filter(personID = request.user.id, date_recorded = new_day)
        day_potassium = 0
        day_phosphorus = 0
        day_sodium = 0
        day_calcium = 0
        day_protein = 0
        day_sugar = 0
        for info in day_data:
            dfood = Food.objects.get(food_name = info.food_name)
            day_potassium += dfood.potassium * info.amount
            day_phosphorus += dfood.phosphorus * info.amount
            day_sodium += dfood.sodium * info.amount
            day_calcium += dfood.calcium * info.amount
            day_protein += ((dfood.protein * info.amount) * 10)
            day_sugar += ((dfood.sugar * info.amount) * 10)

        #append daily values to week list
        week_potassium.append(day_potassium)
        week_phosphorus.append(day_phosphorus)
        week_sodium.append(day_sodium)
        week_calcium.append(day_calcium)
        week_protein.append(day_protein)
        week_sugar.append(day_sugar)

        
            
    context = {
        'names' : ['Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)', 'Calcium (mg)', 'Protein (cg)', 'Sugar (cg)'],
        'totals' : [potassium, phosphorus, sodium, calcium, protein, sugar],
        'currentUser': Person.objects.get(personID  = request.user.id),
        'protein' : rprotein, 
        'water' : rwater,
        'sugar' : rsugar,
        'wpot' : week_potassium,#[::-1], 
        'wphos' : week_phosphorus,#[::-1], 
        'wsod' : week_sodium,#[::-1], 
        'wcal' : week_calcium,#[::-1], 
        'wpro' : week_protein,#[::-1], 
        'wsug' : week_sugar,#[::-1],
        'alerts' : alerts,
    }
    return render(request, 'dashboard/index.html', context)


def journalEntryAdd(request):
    if request.method == 'POST':
        new_entry = JournalEntry()

        person = Person.objects.get(personID = request.user.id)
        new_entry.personID = person.personID
        new_entry.date_recorded= request.POST['date']
        new_entry.time_recorded = request.POST['time']
        new_entry.food_name = request.POST['food_name']
        new_entry.amount = request.POST['amount']

        new_entry.save()

        if len(Food.objects.filter(food_name = request.POST['food_name'])) <= 0:
            new_food = Food()

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

            if len(json_response['foods']) > 0:
                phosphorus = 0
                sodium = 0
                potassium = 0
                calcium = 0
                protein = 0
                sugar = 0

                for nutrient in json_response['foods'][0]['foodNutrients']:
                    if nutrient['nutrientName'] == 'Phosphorus, P':
                        phosphorus = nutrient['value']
                    if nutrient['nutrientName'] == 'Sodium, Na':
                        sodium = nutrient['value']
                    if nutrient['nutrientName'] == 'Potassium, K':
                        potassium = nutrient['value']
                    if nutrient['nutrientName'] == 'Calcium, Ca':
                        calcium = nutrient['value']
                    if nutrient['nutrientName'] == 'Protein':
                        protein = nutrient['value']
                    if nutrient['nutrientName'] == 'Carbohydrate, by difference':
                        sugar = nutrient['value']

                new_food.serving_size = 100
                new_food.units = 'g'
                new_food.potassium = potassium
                new_food.phosphorus = phosphorus
                new_food.sodium = sodium
                new_food.calcium = calcium
                new_food.protein = protein
                new_food.sugar = sugar

                new_food.save()

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

    if len(Food.objects.filter(food_name = request.POST['search'])) <= 0:
        food_names = []
        serving_sizes = []
        if len(response.json()['foods']) > 0:
            for food in json_response['foods']:
                food_names.append(food['description'])
                serving_sizes.append('100 g')
    else:
        food_names = []
        serving_sizes = []

        for food in Food.objects.filter(food_name = request.POST['search']):
            food_names.append(food.food_name)
            serving_sizes.append(str(food.serving_size) + " " + str(food.units))

        if len(response.json()['foods']) > 0:
            for food in json_response['foods']:
                if food['description'] not in food_names:
                    food_names.append(food['description'])
                    serving_sizes.append('100 g')

    context = {
        'food_names' : food_names,
        'serving_sizes' : serving_sizes,
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


def entriesPageView(request) :
    data = JournalEntry.objects.filter(personID = request.user.id)
    data_array = []
    for dates in data:
        if dates.date_recorded not in data_array:
            data_array.append(dates.date_recorded)

    data_array = sorted(data_array, reverse=True)

    context = {
        "journal_entries" : data,
        'currentUser': Person.objects.get(personID  = request.user.id),
        'data_array' : data_array,
        }
    return render(request, 'dashboard/entries.html', context)


def updateEntries(request, journalID):
    context = {
        "currentUser" : Person.objects.get(personID  = request.user.id),
        "currentEntry" : JournalEntry.objects.get(journalID = journalID)
    }
    return render(request, "dashboard/updateEntries.html", context)


def updateJournalEntry(request): 

    entry = JournalEntry.objects.get(journalID = request.POST['journalid'])

    entry.food_name = request.POST['food_name']
    entry.date_recorded = request.POST['date']
    entry.time_recorded = request.POST['time']
    entry.amount = request.POST['amount']

    entry.save()

    if len(Food.objects.filter(food_name = request.POST['food_name'])) <= 0:
        new_food = Food()           
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

        if len(response.json()['foods']) > 0:
            phosphorus = 0
            sodium = 0
            potassium = 0
            calcium = 0
            protein = 0
            sugar = 0

            for nutrient in json_response['foods'][0]['foodNutrients']:
                if nutrient['nutrientName'] == 'Phosphorus, P':
                    phosphorus = nutrient['value']
                if nutrient['nutrientName'] == 'Sodium, Na':
                    sodium = nutrient['value']
                if nutrient['nutrientName'] == 'Potassium, K':
                    potassium = nutrient['value']
                if nutrient['nutrientName'] == 'Calcium, Ca':
                    calcium = nutrient['value']
                if nutrient['nutrientName'] == 'Protein':
                    protein = nutrient['value']
                if nutrient['nutrientName'] == 'Carbohydrate, by difference':
                    sugar = nutrient['value']

            new_food.serving_size = 100
            new_food.units = 'g'
            new_food.potassium = potassium
            new_food.phosphorus = phosphorus
            new_food.sodium = sodium
            new_food.calcium = calcium
            new_food.protein = protein
            new_food.sugar = sugar

            new_food.save()

    return redirect("entries")

def editFoodItemEntry(request):
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

    return render(request, 'dashboard/updateEntries.html')

def deleteJournalEntry(request, journalID):
    entry = JournalEntry.objects.get(journalID = journalID)
    entry.delete()
    return redirect('entries')

def foodSearchUpdateJournal(request, journalID):

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

    if len(Food.objects.filter(food_name = request.POST['search'])) <= 0:
        food_names = []
        serving_sizes = []
        if len(response.json()['foods']) > 0:
            for food in json_response['foods']:
                food_names.append(food['description'])
                serving_sizes.append('100 g')
    else:
        food_names = []
        serving_sizes = []

        for food in Food.objects.filter(food_name = request.POST['search']):
            food_names.append(food.food_name)
            serving_sizes.append(str(food.serving_size) + " " + str(food.units))

        if len(response.json()['foods']) > 0:
            for food in json_response['foods']:
                if food['description'] not in food_names:
                    food_names.append(food['description'])
                    serving_sizes.append('100 g')

    context = {
        'food_names' : food_names,
        'serving_sizes' : serving_sizes,
        "currentEntry" : JournalEntry.objects.get(journalID = journalID)
    }

    return render(request, 'dashboard/updateEntries.html', context)
    