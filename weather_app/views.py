from requests import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import WeatherRequestSerializer
from .weather_service import WeatherService

@api_view(['POST'])
def post_weather(request: Request) -> Response:
    serializer = WeatherRequestSerializer(data=request.data)
    return make_request(serializer)

@api_view(['GET'])
def get_weather_city(request: Request, city = None) -> Response:
    serializer = WeatherRequestSerializer(data={"city": city})
    return make_request(serializer)

@api_view(['GET'])
def get_weather_cords(request: Request, lantitude: float = None, longitude: float = None) -> Response:
    serializer = WeatherRequestSerializer(data=request.query_params)
    return make_request(serializer)

def make_request(serializer: WeatherRequestSerializer) -> Response:
    if serializer.is_valid():
        city: str = serializer.validated_data.get("city")
        lantitude: float = serializer.validated_data.get("lantitude")
        longitude: float = serializer.validated_data.get("longitude")

        # Fetch weather using service function
        try:
            weather_info = WeatherService.request_weather(city, lantitude, longitude)
            return Response(weather_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    