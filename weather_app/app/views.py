from django.shortcuts import render
import requests
import datetime

def index(request):
    API_KEY = '95cc09057dc7a14a3a6fadc9b7855f0f'
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric'

    if request.method == 'POST':
        city1 = request.POST.get('city1')

        weather_data1, daily_forecast1 = fetch_weather_and_forecast(city1, API_KEY, weather_url, forecast_url)

        context = {
            "weather_data1": weather_data1,
            "daily_forecast": daily_forecast1
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html')

def fetch_weather_and_forecast(city, api_key, weather_url, forecast_url):
    response = requests.get(weather_url.format(city, api_key)).json()
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp']),
        "day": datetime.datetime.fromtimestamp(response['dt']).strftime('%A'),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
        "humidity": response['main']['humidity'],
        "pressure": response['main']['pressure'],
        "wind": response['wind']['speed']
    }

    daily_forecast = []
    for i in range(8, len(forecast_response['list']), 8):
        daily_forecast.append({
            "day": datetime.datetime.fromtimestamp(forecast_response['list'][i]['dt']).strftime('%A'),
            "max_temp": round(forecast_response['list'][i]['main']['temp_max']),
            "description": forecast_response['list'][i]['weather'][0]['description'],
            "icon": forecast_response['list'][i]['weather'][0]['icon']
        })

    last_index = len(forecast_response['list']) - 1
    daily_forecast.append({
        "day": datetime.datetime.fromtimestamp(forecast_response['list'][last_index]['dt']).strftime('%A'),
        "max_temp": round(forecast_response['list'][last_index]['main']['temp_max']),
        "description": forecast_response['list'][last_index]['weather'][0]['description'],
        "icon": forecast_response['list'][last_index]['weather'][0]['icon']
    })

    return weather_data, daily_forecast

    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    
