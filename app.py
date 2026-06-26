import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from supabase import create_client
from datetime import datetime, timedelta

# --- 1. 設定與初始化 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
st.title("🐱 咪姐的永久秘密基地")

# 初始化服務 (確保 Secrets 已設定)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel("gemini-3.5-flash")
except Exception as e:
    st.error(f"系統初始化失敗: {e}")

# --- 2. 天氣偵測函數 ---
def get_weather(city="Zhongli"):
    try:
        api_key = st.secrets["WEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
        res = requests.get(url).json()
        if res.get("cod") == 200:
            return f"{res['weather'][0]['description']}, 氣溫 {res['main']['temp']}°C"
    except:
        return "晴朗涼爽"
    return "晴朗涼爽"

# --- 3. AI 翻譯區塊 ---
st.subheader("📸 咪姐心情翻譯機")
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="咪姐正在看你...", use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        with st.spinner('翻譯官思考中...'):
            weather_info = get_weather()
            # 條件式語氣判斷
            if "雨" in weather_info or "冷" in weather_info:
                tone = "極度傲嬌、毒舌、不耐煩"
            else:
                tone = "傲嬌、愛理不理"
            
            prompt = f"請用{tone}的口吻描述這隻貓咪心情。今日天氣是{weather_info}，請將天氣融入回覆中並調整語氣。"
            
            try:
                response = model.generate_content([prompt, image])
                st.write(f"### 💬 翻譯官：咪姐說：\n{response.text}")
            except Exception as e:
                st.error(f"翻譯官罷工了：{e}")

st.divider()

# --- 4. 永久留言板 (Supabase) ---
st.subheader("📝 罐罐日記")
try:
    response = supabase.table("diary").select("*").order("id", desc=True).execute()
    for msg in response.data:
        st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
except Exception as e:
    st.error(f"讀取失敗: {e}")

new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        time_str = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        try:
            supabase.table("diary").insert({"timestamp": time_str, "message": new_msg}).execute()
            st.success("留言已送達！")
            st.rerun()
        except Exception as e:
            st.error(f"寫入失敗：{e}")
