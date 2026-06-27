import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from supabase import create_client
from datetime import datetime, timedelta
import time

# --- 0. 初始化設定 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.attempts = 0
    st.session_state.lockout_time = None
    st.session_state.last_login_date = None

# --- 1. 安檢防護門 (每日重置 & 錯誤鎖定) ---
# 每日午夜重置
if st.session_state.authenticated:
    if st.session_state.last_login_date != datetime.now().date():
        st.session_state.authenticated = False
        st.rerun()

# 錯誤三次鎖定 24 小時
if st.session_state.attempts >= 3:
    if st.session_state.lockout_time and (datetime.now() - st.session_state.lockout_time) < timedelta(hours=24):
        st.error("❌ 你已經失敗三次，請 24 小時後再來挑戰！")
        st.stop()
    else:
        st.session_state.attempts = 0
        st.session_state.lockout_time = None

# 登入介面
if not st.session_state.authenticated:
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼才能進入", type="password")
    if st.button("解鎖"):
        if password == "Meow123":
            st.session_state.authenticated = True
            st.session_state.attempts = 0
            st.session_state.last_login_date = datetime.now().date()
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.lockout_time = datetime.now()
            st.error(f"密碼錯誤！剩餘機會: {3 - st.session_state.attempts}")
    st.stop()

# --- 2. 秘密基地內容 ---
st.title("🐱 咪姐的永久秘密基地")

# 初始化工具
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash") # 確保使用正確模型名稱

def get_weather(city="Zhongli"):
    try:
        api_key = st.secrets["WEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
        res = requests.get(url).json()
        if res.get("cod") == 200:
            return f"{res['weather'][0]['description']}, 氣溫 {res['main']['temp']}°C"
    except: return "晴朗涼爽"
    return "晴朗涼爽"

st.subheader("📸 咪姐心情翻譯機")
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        with st.spinner('翻譯官思考中...'):
            weather_info = get_weather()
            tone = "極度傲嬌、毒舌、不耐煩" if any(x in weather_info for x in ["雨", "冷"]) else "傲嬌、愛理不理"
            prompt = f"請用{tone}口吻描述貓咪心情。今日天氣是{weather_info}。請嚴格按照以下格式回覆：\n【傲嬌指數】：X/10\n【翻譯心聲】：(內容)"
            
            try:
                response = model.generate_content([prompt, image])
                st.write(f"### 💬 翻譯官：咪姐說：\n{response.text}")
            except Exception as e:
                st.warning("咪姐現在不想理人（API 限制），請稍後再試！")

st.divider()
st.subheader("📝 罐罐日記")
try:
    response = supabase.table("diary").select("*").order("id", desc=True).execute()
    for msg in response.data:
        st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
except: st.error("日記本暫時打不開")

new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        time_str = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        supabase.table("diary").insert({"timestamp": time_str, "message": new_msg}).execute()
        st.rerun()
