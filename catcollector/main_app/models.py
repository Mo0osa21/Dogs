from django.db import models

class Dog(models.Model):
    name=models.CharField(max_length=100)
    breed=models.CharField(max_length=100)
    describtion = models.TextField(max_length=250)
    age = models.IntegerField()
    image=models.ImageField(upload_to='main_app/static/upload/',default="")