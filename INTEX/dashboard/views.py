from django.shortcuts import render, redirect
from .models import Person
from .forms import MovieDataForm
 
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
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = IdeaForm()
    context = {
        'data': data,
        'form': form,
    }
    return render(request, 'dashboard/input.html', context)

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
	return redirect("dashboard-index")
 
def indexPageView(request):
    data = MovieData.objects.all()
    if request.method == 'POST':
        form = MovieDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MovieDataForm()
    context = {
        'data': data,
        'form': form,
    }
    return render(request, 'dashboard/index.html', context)