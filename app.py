import streamlit as st
import google.generativeai as genai
from supabase import create_client
from datetime import datetime, timedelta

# --- 0. 最底層的狀態初始化 (確保不被洗掉) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "last_login" not in st.session_state:
    st.session_state.last_login = None

def get_tw_date(): 
    return (datetime.utcnow() + timedelta(hours=8)).date()

# --- 1. 認證檢查邏輯 (防禦性檢查) ---
# 只有在明確符合登入條件時才將其視為 True
def is_logged_in():
    if not st.session_state.authenticated:
        return False
    # 檢查是否跨日
    if st.session_state.last_login != get_tw_date():
        st.session_state.authenticated = False
        st.session_state.last_login = None
        return False
    return True

# --- 2. 登入介面 ---
if not is_logged_in():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼", type="password")
    if st.button("解鎖"):
        if password == "71398426":
            st.session_state.authenticated = True
            st.session_state.last_login = get_tw_date()
            st.rerun()
        else:
            st.error("密碼錯誤")
    st.stop() # 確保登入成功前，下方程式碼完全不執行

# --- 3. 核心功能區 (只有認證成功才到這裡) ---
st.title("🐱 咪姐的永久秘密基地")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 顯示好感度
try:
    score = supabase.table("diary").select("id", count='exact').execute().count or 0
    st.write(f"目前與咪姐的好感度：**{score}** 點")
except:
    score = 0

# (以下維持你原本的拍照與日記功能)
# 日記區
st.divider()
st.subheader("📝 罐罐日記")
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        supabase.table("diary").insert({"timestamp": datetime.now().strftime("%m/%d %H:%M"), "message": new_msg}).execute()
        st.rerun()

data = supabase.table("diary").select("*").order("id", desc=True).execute().data
for msg in data: st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
