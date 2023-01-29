from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fairmap', views.show_fairmap, name='show_fairmap'),
    path('survey', views.survey, name='survey'),
    path('ranking', views.ranking, name='ranking'),
    path('about', views.about, name='about'),
    path('open_data', views.open_data, name='open_data'),
    path('location_detail/<str:latitude>/<str:longitude>', views.get_location_detail, name='location_detail'),   
]
