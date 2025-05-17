import requests
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from bs4 import BeautifulSoup
from datetime import datetime
from kivy.core.window import Window
Window.size = (350, 700)

class WeatherApp(MDApp):
    api_key = "paste your api here" # OpenWeatherMap API key

    def on_start(self): 
        try:
            response = requests.get("https://www.google.com/search?q=my+current+location+weather")
            soup = BeautifulSoup(response.text, "html.parser")
            temp = soup.find("span", {"class": "BNeawe", "role": "heading"})

            if temp is not None:
                location = ''.join(filter(lambda item: not item.isdigit(), temp.text)).split(",", 1)
                self.get_weather(location[0])
            else:
                self.show_error("Could not retrieve weather information. Please check the HTML structure.")
        except requests.ConnectionError:
            self.show_error("No Internet Connection")

    def build(self):
        bldr=Builder.load_file("ui.kv")
        return bldr

    def get_weather(self, city_name):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"
            response = requests.get(url)
            x = response.json()
            if x["cod"] != "404":
                id = int(x["weather"][0]["id"])
                self.root.ids.temperature.text = f"[b]{round(x["main"]["temp"] - 273.15)}[/b]°"
                self.root.ids.weather.text = str(x["weather"][0]["main"])
                self.root.ids.humidity.text = f"{x["main"]["humidity"]}%"
                self.root.ids.wind_speed.text = f"{round(x["wind"]["speed"] * 18 / 5)}km/h"
                self.root.ids.location.text =x["name"] + ", " + x["sys"]["country"]

                sunrise_time = datetime.fromtimestamp(x["sys"]["sunrise"]).strftime('%I:%H %p')
                sunset_time = datetime.fromtimestamp(x["sys"]["sunset"]).strftime('%I:%H %p')
                self.root.ids.sunrise.text = f"Sunrise {sunrise_time}"
                self.root.ids.sunset.text = f"Sunset {sunset_time}"

                if id == 800:
                    self.root.ids.weather_image.source = "assets/sun.png"
                elif 200 <= id <= 232:
                    self.root.ids.weather_image.source = "assets/storm.png"
                elif 300 <= id <= 321:
                    self.root.ids.weather_image.source = "assets/drizzle.png"
                elif 600 <= id <= 622:
                    self.root.ids.weather_image.source = "assets/snow.png"
                elif 701 <= id <= 781:
                    self.root.ids.weather_image.source = "assets/haze.png"
                elif 801 <= id <= 804:
                    self.root.ids.weather_image.source = "assets/cloud.png"
            else:
                self.show_error("City Not Found!")
        except (requests.ConnectionError,KeyError):
            self.show_error("No Internet Connection!")

    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name:
            self.get_weather(city_name)

    def show_error(self, message):
        # Implement a method to display error messages in the app's UI
        print(message)

if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="/Users/amit/Developer/py virtual/myenv/Weather-app/assets/font/Poppins-Regular.ttf")
    LabelBase.register(name="LPoppins", fn_regular="/Users/amit/Developer/py virtual/myenv/Weather-app/assets/font/Poppins-MediumItalic.ttf")
    WeatherApp().run()
