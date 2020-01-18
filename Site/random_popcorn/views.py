from time import gmtime
# Create your views here.
from time import strftime

from bootstrap_modal_forms.generic import BSModalReadView
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.shortcuts import HttpResponseRedirect, reverse, render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserRegisterForm, UserLoginForm, AddMovieTable, AccountImageForm
from .models import Movie, AccountProfile
from .serializers import MovieSerializer, AccountSerializer


def ConvertTime(min):
    watch_time = {
        'month': int(strftime("%m", gmtime(min * 60))) - 1,
        'day': int(strftime("%d", gmtime(min * 60))) - 1,
        'hour': strftime("%H", gmtime(min * 60)),
        'min': strftime("%M", gmtime(min * 60)),
    }
    return watch_time


def index(request):
    return render(request, "index.html")


def updatePicture(request):
    accountProfile = AccountProfile.objects.get(user=request.user)
    if request.method == "POST":
        imageForm = AccountImageForm(data=request.POST, instance=accountProfile)
        if imageForm.is_valid():
            profile = imageForm.save(commit=False)
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
    else:
        imageForm = AccountImageForm(instance=accountProfile)

    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))


def account_profile(request, user_id):
    try:
        accountInfo = AccountProfile.objects.get(pk=user_id)
        movieTable = AddMovieTable(Movie.objects.all())
        movieCount = accountInfo.movies.count()
        watchedMovieCount = accountInfo.watchedMovies.count()
        # num_results = accountInfo.watchedMovies.filter(id=accountInfo.movies.).count()

        time = 0

        for timeMovie in accountInfo.watchedMovies.all():
            time = time + int(timeMovie.runtime)

        context = {'accountInfo': accountInfo, 'movieTable': movieTable,
                   'stats': {'movieCount': movieCount,
                             'watchedMovieCount': watchedMovieCount,
                             'watch_time': ConvertTime(time)}}
        return render(request, 'user_profile.html', context)
    except AccountProfile.DoesNotExist:
        return render(request, "404.html", {'error': 'User not found'})


def addMovie(request, user_id, tab):  # 0 - myMovies / 1 - watchedMovies
    info = AccountProfile.objects.get(pk=user_id)

    if request.method == "POST":
        moviesSelected = request.POST.getlist("selection")
        for movie in moviesSelected:
            if tab == 0:
                info.movies.add(movie)
            else:
                info.watchedMovies.add(movie)

    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


def removeMovie(request, user_id, movie_id, tab):  # 0 - myMovies / 1 - watchedMovies
    info = AccountProfile.objects.get(pk=user_id)

    if request.method == "POST":
        if tab == 0:
            info.movies.remove(movie_id)
        else:
            info.watchedMovies.remove(movie_id)

    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


class InfoMovie(BSModalReadView):
    model = Movie
    template_name = 'dialog-info.html'


def signup_view(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            django_login(request, new_user)
            return redirect('/')
    context = {'form': form}
    return render(request, 'sign_up.html', context)


def login(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            django_login(request, user)
            return redirect('/')

    context = {'form': form}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


class MovieDetail(APIView):
    """Lists a Movie."""

    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)


class RandomMovie(APIView):
    """Random Movie"""
    queryset = Movie.objects.all()
    model = Movie
    serializer_class = MovieSerializer

    def get(self, request, pk=None):
        movie = Movie.objects.order_by('?').first()
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = AccountProfile.objects.all()
    serializer_class = AccountSerializer
