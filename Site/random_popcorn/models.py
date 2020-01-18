from django.contrib.auth.models import User as UserDJ
from django.db import models
from django.db.models.signals import post_save


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Language(models.Model):
    country = models.CharField(max_length=50)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language


class Movie(models.Model):
    title = models.CharField(max_length=100)
    runtime = models.IntegerField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    languages = models.ManyToManyField(Language)
    plot = models.CharField(max_length=5000)
    rating_imdb = models.FloatField()
    poster = models.CharField(max_length=254)

    def __str__(self):
        return self.title


class AccountProfile(models.Model):
    user = models.OneToOneField(UserDJ, on_delete=models.CASCADE)
    locality = models.CharField(max_length=100, default="", blank=True)
    picture = models.ImageField(upload_to='account_image', blank=True)
    movies = models.ManyToManyField(Movie, blank=True, related_name='movies')
    watchedMovies = models.ManyToManyField(Movie, blank=True, related_name='watched')

    def __str__(self):
        return self.user.email


def create_profile(sender, **kwargs):
    if kwargs['created']:
        AccountProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=UserDJ)
