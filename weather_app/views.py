from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from .serializers import WeatherDataSerializer, WeatherRequestSerializer
from .models import WeatherData
from .weather_service import WeatherService

@api_view(['POST'])
def weather(request):
    serializer = WeatherRequestSerializer(data=request.data)
    if serializer.is_valid():
        city: str = serializer.validated_data.get("city")
        lantitude: float = serializer.validated_data.get("lantitude")
        longitude: float = serializer.validated_data.get("longitude")

        # Fetch weather using service function
        try:
            weather_info = WeatherService.fetch_weather(city, lantitude, longitude)
            return Response(weather_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)