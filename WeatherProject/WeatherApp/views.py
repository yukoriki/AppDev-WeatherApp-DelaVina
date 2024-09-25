from django.shortcuts import render, HttpResponse
import urllib.request
import json
from urllib.parse import quote
from .models import Weather 

# Create your views here.
def index(request):
    weather_records = Weather.objects.all().order_by('-created_at')[:5]  # Fetch last 5 records

    if request.method == 'POST':
        city = request.POST['city']
        city = city.replace(" ", "%20")

        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=c959fad9d9b90d4901eaef9110ea3d01').read()
        list_of_data = json.loads(source)

        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinates": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temperature": list_of_data['main']['temp'],
            "pressure": list_of_data['main']['pressure'],
            "humidity": list_of_data['main']['humidity'],
            'weather_main': str(list_of_data['weather'][0]['main']),
            'weather_description': str(list_of_data['weather'][0]['description']),
            'weather_icon': list_of_data['weather'][0]['icon'],
        }

        weather_record = Weather.objects.create(
            city=city,
            country_code=data['country_code'],
            coordinates=data['coordinates'],
            temperature=data['temperature'],
            pressure=data['pressure'],
            humidity=data['humidity'],
            weather_main=data['weather_main'],
            weather_description=data['weather_description'],
            weather_icon=data['weather_icon']
        )

        context = {
            'country_code': data['country_code'],
            'coordinate': data['coordinates'],
            'temp': data['temperature'],
            'pressure': data['pressure'],
            'humidity': data['humidity'],
            'main': data['weather_main'],
            'description': data['weather_description'],
            'icon': data['weather_icon'],
            'weather_record': weather_record,
            'weather_records': weather_records,
        }
    else:
        context = {'weather_records': weather_records}

    return render(request, "index.html", context)