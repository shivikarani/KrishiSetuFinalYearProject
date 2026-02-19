import requests

OPENWEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'

def get_weather(city_name):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_list = []
        for item in data['list'][:7]:  # 7-day forecast
            forecast_list.append({
                'date': item['dt_txt'],
                'temp': item['main']['temp'],
                'weather': item['weather'][0]['description'],
                'rain': item.get('rain', {}).get('3h', 0)
            })
        return forecast_list
    return []



def get_market_prices(crop_name=None):
    # Example: Use a govt API or dummy data
    api_url = 'https://api.example.com/market-prices'
    response = requests.get(api_url)
    prices = []
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if not crop_name or crop_name.lower() in item['crop'].lower():
                prices.append(item)
    return prices



# Simple example using a keyword-based approach
def chatbot_response(user_message):
    faq = {
        "wheat": "Wheat should be sown in November-December in North India.",
        "rice": "Rice requires 150-200 days for full growth.",
        "fertilizer": "Apply 20kg nitrogen per hectare for wheat.",
        "pest": "Use neem-based pesticide to control pests."
    }

    message = user_message.lower()
    for key, response in faq.items():
        if key in message:
            return response
    return "Sorry, our experts will respond soon. You can also submit your query."

