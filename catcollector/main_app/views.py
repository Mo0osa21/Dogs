from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dog
from .models import Toy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView,DetailView
from .forms import FeedingForm

class DogCreate(CreateView):
    model=Dog
    # fields = '__all__'
    fields=['name','breed','describtion','age','image']
    # success_url ='/dogs/'

class DogUpdate(UpdateView):
    model=Dog
    # fields = '__all__'
    fields=['breed','describtion','age']
    # success_url ='/dogs/'

class DogDelete(DeleteView):
    model=Dog
    success_url ='/dogs/'


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
def dog_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    feeding_form = FeedingForm()
    toys_dog_dosent_have=Toy.objects.exclude(id__in=dog.toys.all().values_list('id'))
    return render(request, 'dogs/detail.html', {'dog': dog, 'feeding_form':feeding_form,'toys':toys_dog_dosent_have})
def add_feeding(request, dog_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)

class ToyList(ListView):
    model=Toy
class ToyDetail(DetailView):
    model=Toy
class ToyCreate(CreateView):
    model=Toy
    fields='__all__'
class ToyUpdate(UpdateView):
    model=Toy
    fields=['name','color']
class ToyDelete(DeleteView):
    model=Toy
    success_url='/toys/'

def assoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)

def unassoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.remove(toy_id)
  return redirect('detail', dog_id=dog_id)
