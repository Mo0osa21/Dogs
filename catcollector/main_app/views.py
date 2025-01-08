from django.shortcuts import render
from django.http import HttpResponse
from .models import Dog
# Create your views here.
def home(request):
    return HttpResponse('<h1>Hello cat collector</h1>')
def about(request):
    return render(request, 'about.html')
def base(request):
    return render(request, 'base.html')
def dog_index(request):
    # Select * from main_app_cat
    dogs=Dog.objects.all()
    return render(request, 'dogs/index.html', {'dogs':dogs})