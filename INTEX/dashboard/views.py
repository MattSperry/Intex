from django.shortcuts import render, redirect
from .models import Person
from .forms import MovieDataForm
 
# Create your views here.
 
def index(request):
    data = Person.objects.all()
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