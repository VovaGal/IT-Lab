# weather app
import requests

# set target city, set APPID
s_city = "Moscow,RU"
appid = "cfb7918104f3072fa401761119d8434b"

# server request today
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
             params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

# server request forecast
res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data1 = res.json()

# data shown

#print(data)

print("Город:", s_city)
print("\nНа сегодня:")
print("Видимость:", data['visibility'])
print("Скорость ветра:", data['wind']['speed'])
#print("Погодные условия:", data['weather'][0]['description'])
#print("Температура:", data['main']['temp'])
#print("Минимальная температура:", data['main']['temp_min'])
#print("Максимальная температура", data['main']['temp_max'])

print("\nНа неделю:")
for i in data1['list']:
    print("Дата <", i['dt_txt'], "> \r\nВидимость <", '{0:+3.0f}'.format(i['visibility']), "> \r\nСкорость ветра <", i['wind']['speed'], ">")


