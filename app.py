import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from supabase import create_client
from datetime import datetime, timedelta

# --- 0. 密碼鎖防護機制 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.attempts = 0
    st.session_state.lockout_time = None

if st.session_state.attempts >= 3:
    if st.session_state.lockout_time and (datetime.now() - st.session_state.lockout_time) < timedelta(hours=24):
        st.error("❌ 你已經失敗三次，請 24 小時後再來！")
        st.stop()
    else:
        st.session_state.attempts = 0
        st.session_state.lockout_time = None

if not st.session_state.authenticated:
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼才能進入", type="password")
    if st.button("解鎖"):
        if password == "71398426": # 請設定你的密碼
            st.session_state.authenticated = True
            st.session_state.attempts = 0
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.lockout_time = datetime.now()
            st.error(f"密碼錯誤！剩餘機會: {3 - st.session_state.attempts}")
    st.stop()

# --- 1. 設定與初始化 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
st.title("🐱 咪姐的永久秘密基地")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-3.5-flash")

# --- 2. 天氣偵測函數 ---
def get_weather(city="Zhongli"):
    try:
        api_key = st.secrets["WEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
        res = requests.get(url).json()
        if res.get("cod") == 200:
            return f"{res['weather'][0]['description']}, 氣溫 {res['main']['temp']}°C"
    except: return "晴朗涼爽"
    return "晴朗涼爽"

# --- 3. AI 翻譯區塊 ---
st.subheader("📸 咪姐心情翻譯機")
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        with st.spinner('翻譯官思考中...'):
            weather_info = get_weather()
            tone = "極度傲嬌、毒舌、不耐煩" if any(x in weather_info for x in ["雨", "冷"]) else "傲嬌、愛理不理"
            prompt = f"""
請用{tone}的口吻描述貓咪心情。
今日天氣是{weather_info}。

請嚴格按照以下格式回覆：
【傲嬌指數】：X/10 (請給予 1 到 10 的傲嬌分數，越傲嬌分數越高)
【翻譯心聲】：(這裡放你傲嬌的描述)
"""
            response = model.generate_content([prompt, image])
            raw_text = response.text
            st.write(f"### 💬 咪姐說：\n{raw_text}")
            
            # 從 AI 的回覆中提取分數 (假設 AI 乖乖照格式回覆)
            try:
                score = int(raw_text.split("【傲嬌指數】：")[1].split("/10")[0])
                time_str = datetime.now().strftime("%m/%d %H:%M")
                
                # 自動存入心情紀錄表
                supabase.table("mood_log").insert({
                    "timestamp": time_str, 
                    "mood_score": score,
                    "message": raw_text
                }).execute()
            except:
                pass # 忽略格式錯誤
            response = model.generate_content([prompt, image])
            st.write(f"### 💬 翻譯官：咪姐說：\n{response.text}")

st.divider()

# --- 4. 永久留言板 ---
st.subheader("📝 罐罐日記")
try:
    response = supabase.table("diary").select("*").order("id", desc=True).execute()
    for msg in response.data:
        st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
except Exception as e: st.error("讀取失敗")

new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        time_str = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        supabase.table("diary").insert({"timestamp": time_str, "message": new_msg}).execute()
        st.rerun()
st.subheader("📊 咪姐傲嬌指數走勢")
mood_data = supabase.table("mood_log").select("mood_score").execute()
if mood_data.data:
    import pandas as pd
    df = pd.DataFrame(mood_data.data)
    st.line_chart(df["mood_score"])
