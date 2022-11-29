from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from .models import Person, JournalEntry
from .forms import UserForm, PersonForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
 
 
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
    return render(request, 'dashboard/input.html', context)

def updateInfoView(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    # fetch the object related to passed id
    obj = get_object_or_404(PersonForm, id = id)
    # pass the object as instance in form
    form = PersonForm(request.POST or None, instance = obj)
    # save the data from the form and
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/index"+id)
    # add form dictionary to context
    context["form"] = form
    return render(request, "dashboard/input.html", context)

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
        food_name = request.POST.get(food_name)
        new_entry.food_name = food_name
        new_entry.save()

    return redirect('/')

    

