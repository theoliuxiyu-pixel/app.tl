import streamlit as st
import requests

def get_weather_commentary(city="Zhongli"):
    """使用 WEATHER_API_KEY 取得天氣並轉譯成咪姐的傲嬌話語"""
    api_key = st.secrets.get("WEATHER_API_KEY") # 確保這裡對應到你 Secrets 中的名稱
    
    if not api_key:
        return "本喵沒看到天氣金鑰，是不是你忘記餵食了？"
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        temp = response['main']['temp']
        
        # 根據溫度回應
        if temp > 30:
            return f"外面 {temp}°C，熱得想把毛脫掉，主人你自己去流汗吧。"
        elif temp < 18:
            return f"現在 {temp}°C，冷颼颼的，這種天氣最適合躲在棉被裡睡覺了，快過來。"
        else:
            return f"外面 {temp}°C，溫度剛剛好，看在天氣不錯的份上，准許你摸我一下。"
    except:
        return "氣象站罷工了，本喵也懶得看。"
