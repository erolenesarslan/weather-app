import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
api_key = os.getenv("API_KEY")

# Main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.config(bg="#1E1E1E")
root.resizable(False, False)

# UI Components
tk.Label(root, text="Enter City", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E").pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14), width=30)
city_entry.pack(pady=5)

icon_label = tk.Label(root, bg="#1E1E1E")
icon_label.pack()

result_text = tk.Label(root, font=("Arial", 14), fg="white", bg="#1E1E1E", justify="left")
result_text.pack(pady=10)

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': api_key}
        response = requests.get(url, params=params)
        data = response.json()
        if data["cod"] != 200:
            raise Exception()

        weather = data['weather'][0]
        main = data['main']
        wind = data['wind']

        description = weather['description'].title()
        temp = round(main['temp'] - 273.15, 1)
        feels_like = round(main['feels_like'] - 273.15, 1)
        humidity = main['humidity']
        wind_speed = wind['speed']

        icon_code = weather['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_img = Image.open(BytesIO(icon_response.content))
        icon_img = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_img)
        icon_label.image = icon_img

        result = (
            f"📍 {city.title()}\n\n"
            f"{description}\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"🤒 Feels Like: {feels_like}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬️ Wind Speed: {wind_speed} m/s"
        )
        result_text.config(text=result)

    except Exception:
        messagebox.showerror("Error", "City not found or API error.")

tk.Button(root, text="Check Weather", font=("Arial", 12, "bold"),
          command=get_weather, bg="#3A7FF6", fg="white", padx=10, pady=5).pack(pady=10)

root.mainloop()
