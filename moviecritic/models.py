from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Movie_Details(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(default=0)
    boxoffice = models.IntegerField(default=0)
    
    imdb = models.IntegerField(default=0)
    metacritic = models.IntegerField(default=0)
    rottentomatoes = models.IntegerField(default=0)
    
    genre = ArrayField(models.CharField(max_length=15), default=list, size=50)
    director = ArrayField(models.CharField(max_length=25), default=list, size=50)
    lang = ArrayField(models.CharField(max_length=15), default=list, size=50)
    country = ArrayField(models.CharField(max_length=25), default=list, size=50)
    prod = ArrayField(models.CharField(max_length=25), default=list, size=50)
        
    def __str__(self):
        return self.name