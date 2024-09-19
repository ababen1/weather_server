import datetime
from django.db import models

class WeatherRequest(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    lantitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

class WeatherData(models.Model):
    ## Temperature in celsius 
    temperature = models.FloatField()

    ## Humidity in percents
    humidity = models.FloatField()

    ## Wind speed in km\h
    wind_speed = models.FloatField()

    weather_conditions = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.weather_conditions}: {self.temperature}C, humidity: {self.humidity}%, wind speed: {self.wind_speed} km\h"
    