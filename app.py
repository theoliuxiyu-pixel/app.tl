import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from supabase import create_client
from datetime import datetime, timedelta

# --- 0. 初始化設定 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

# 初始化 Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.attempts = 0
    st.session_state.lockout_time = None
    st.session_state.last_login_date = None

# --- 1. 安檢防護門 (台灣時間 UTC+8) ---
def get_tw_date(): return (datetime.utcnow() + timedelta(hours=8)).date()

if st.session_state.authenticated:
    if st.session_state.last_login_date != get_tw_date():
        st.session_state.authenticated = False
        st.rerun()

if st.session_state.attempts >= 3:
    if st.session_state.lockout_time and (datetime.utcnow() + timedelta(hours=8) - st.session_state.lockout_time) < timedelta(hours=24):
        st.error("❌ 嘗試次數過多，請 24 小時後再來。")
        st.stop()
    else:
        st.session_state.attempts = 0
        st.session_state.lockout_time = None

if not st.session_state.authenticated:
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼", type="password")
    if st.button("解鎖"):
        if password == "71398426":
            st.session_state.authenticated = True
            st.session_state.last_login_date = get_tw_date()
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.lockout_time = datetime.utcnow() + timedelta(hours=8)
            st.error("密碼錯誤")
    st.stop()

# --- 2. 核心功能與資料庫 ---
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 好感度邏輯：統計日記留言數
def get_loyalty_score():
    try:
        data = supabase.table("diary").select("id", count='exact').execute()
        return data.count if data.count else 0
    except: return 0

score = get_loyalty_score()

# 動態風格 CSS
def apply_theme(s):
    bg = "#ffebf0" if s >= 15 else ("#faedcd" if s >= 6 else "#f0f0f0")
    color = "#ffafcc" if s >= 15 else ("#d4a373" if s >= 6 else "#333333")
    st.markdown(f"""<style>.stApp {{ background-color: {bg}; }} h1, h2 {{ color: {color}; }}</style>""", unsafe_allow_html=True)

apply_theme(score)

# --- 3. 頁面內容 ---
st.title("🐱 咪姐的永久秘密基地")
st.write(f"與咪姐的好感度：**{score}** 點")

uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        tone = "溫柔且親暱" if score >= 15 else ("傲嬌但有點害羞" if score >= 6 else "極度傲嬌、毒舌")
        prompt = f"你是一隻貓咪咪姐，目前我們的好感度是{score}。請用{tone}口吻描述這張照片的心情。"
        response = model.generate_content([prompt, image])
        st.write(f"### 💬 咪姐說：\n{response.text}")

st.divider()
st.subheader("📝 罐罐日記")
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        supabase.table("diary").insert({"timestamp": datetime.now().strftime("%m/%d %H:%M"), "message": new_msg}).execute()
        st.rerun()

data = supabase.table("diary").select("*").order("id", desc=True).execute().data
for msg in data: st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
