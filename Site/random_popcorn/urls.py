from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('account', views.AccountViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('account/signup/', views.signup_view, name='signup'),
    path('account/login/', views.login, name='login'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/<int:user_id>/profile/', views.account_profile, name='profile'),

    path('account/<int:user_id>/removeMovie/<int:movie_id>/<int:tab>', views.removeMovie, name='removeMovie'),
    path('account/<int:user_id>/addMovie/<int:tab>', views.addMovie, name='addMovie'),
    path('movieInfo/<int:pk>', views.InfoMovie.as_view(), name='infoMovie'),
    path('account/update', views.update_user, name='update'),

    # Rest API
    url(r'^api/movie/random/', views.RandomMovie.as_view(), name='movie_random'),
    url(r'api/', include(router.urls), name='movie_api')

]
