from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dog
from .models import Toy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView,DetailView
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class DogCreate(LoginRequiredMixin,CreateView):
    model=Dog
    # fields = '__all__'
    fields=['name','breed','describtion','age','image']
    # success_url ='/dogs/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DogUpdate(LoginRequiredMixin,UpdateView):
    model=Dog
    # fields = '__all__'
    fields=['breed','describtion','age']
    # success_url ='/dogs/'

class DogDelete(LoginRequiredMixin,DeleteView):
    model=Dog
    success_url ='/dogs/'

class ToyList(LoginRequiredMixin,ListView):
    model=Toy
class ToyDetail(LoginRequiredMixin,DetailView):
    model=Toy
class ToyCreate(LoginRequiredMixin,CreateView):
    model=Toy
    fields='__all__'
class ToyUpdate(LoginRequiredMixin,UpdateView):
    model=Toy
    fields=['name','color']
class ToyDelete(LoginRequiredMixin,DeleteView):
    model=Toy
    success_url='/toys/'

# Create your views here.
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def base(request):
    return render(request, 'base.html')

@login_required
def dog_index(request):
    # Select * from main_app_cat
    # dogs=Dog.objects.all()
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', {'dogs':dogs})
@login_required
def dog_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    feeding_form = FeedingForm()
    toys_dog_dosent_have=Toy.objects.exclude(id__in=dog.toys.all().values_list('id'))
    return render(request, 'dogs/detail.html', {'dog': dog, 'feeding_form':feeding_form,'toys':toys_dog_dosent_have})
@login_required
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
@login_required
def assoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)
@login_required
def unassoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.remove(toy_id)
  return redirect('detail', dog_id=dog_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)