from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_weather),
    path("coordinates", views.get_weather_cords),
    path("<str:city>", views.get_weather_city),
]
