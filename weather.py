import streamlit as st
import requests

def get_weather_commentary(city="Zhongli"):
    api_key = st.secrets.get("WEATHER_API_KEY")
    if not api_key: return "金鑰沒設好，本喵沒心情看天氣。"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        data = requests.get(url).json()
        temp = data['main']['temp']
        if temp > 30: return f"外面 {temp}°C，熱死人了，你自己去流汗吧。"
        if temp < 18: return f"現在 {temp}°C，冷颼颼的，快滾進棉被裡陪我睡覺。"
        return f"外面 {temp}°C，天氣還行，勉強准許你摸我一下。"
    except: return "氣象站罷工了，懶得看。"
