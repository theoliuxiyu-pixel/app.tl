import streamlit as st
import google.generativeai as genai
import requests
import random
from supabase import create_client
from datetime import datetime, timezone, timedelta
from streamlit_cookies_controller import CookieController 

# --- 0. 初始化 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱", initial_sidebar_state="collapsed")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
cookies = CookieController()

def get_user_ip():
    try: return requests.get('https://api.ipify.org', timeout=2).text
    except: return "unknown"

# --- 1. 模組化函式 ---
def add_to_diary(message):
    try:
        supabase.table("diary").insert({
            "timestamp": datetime.now(timezone(timedelta(hours=8))).strftime("%m/%d %H:%M"), 
            "message": message
        }).execute()
        st.rerun()
    except Exception as e:
        st.error(f"寫入失敗: {e}")

def check_auth_and_cooldown():
    if cookies.get("is_authenticated") == "True":
        return True
    user_ip = get_user_ip()
    try:
        res = supabase.table("auth_log").select("status, last_attempt_time").eq("session_id", user_ip).execute()
        if len(res.data) > 0 and res.data[0]['status'] == True: return True
    except: pass
    return False

# --- 2. 登入系統 ---
if not check_auth_and_cooldown():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼", type="password")
    if st.button("解鎖"):
        if password == "71398426":
            cookies.set("is_authenticated", "True", max_age=365 * 24 * 3600)
            st.rerun()
        else:
            st.error("密碼錯誤！")
    st.stop()

# --- 3. 主介面 ---
st.title("🐱 咪姐的永久秘密基地")

# 好感度統計
score = supabase.table("diary").select("id", count='exact').execute().count or 0
st.write(f"目前好感度：**{score}**")

# 猜拳遊戲
with st.expander("🥊 挑戰咪姐猜拳"):
    options = ["剪刀", "石頭", "布"]
    user_choice = st.radio("你出什麼？", options, horizontal=True)
    if st.button("確認出拳"):
        mi_choice = random.choice(options)
        st.write(f"咪姐出了：**{mi_choice}**")
        if (user_choice == "剪刀" and mi_choice == "布") or (user_choice == "石頭" and mi_choice == "剪刀") or (user_choice == "布" and mi_choice == "石頭"):
            st.success("🎉 贏了！好感度+1")
            add_to_diary("在猜拳中贏過了咪姐，獲得好感度！")
        elif user_choice == mi_choice: st.info("平手！")
        else: st.error("嗚嗚，咪姐贏了！")

# Emoji 互動區
st.write("DEBUG: 正在嘗試渲染 Emoji 選單...")
st.subheader("💬 與咪姐互動")
with st.popover("😊 送個表情給咪姐"):
    cols1 = st.columns(4)
    for i, emoji in enumerate(["❤️", "✨", "🥰", "🐱"]):
        if cols1[i].button(emoji, key=f"m_{i}"): add_to_diary(f"送給咪姐一個 {emoji}")
    cols2 = st.columns(4)
    for i, emoji in enumerate(["🐟", "💤", "🧶", "🐾"]):
        if cols2[i].button(emoji, key=f"a_{i}"): add_to_diary(f"送給咪姐一個 {emoji}")

# 日記區
st.subheader("📝 罐罐日記")
with st.container(height=300):
    for msg in supabase.table("diary").select("*").order("id", desc=True).execute().data:
        st.caption(f"{msg.get('timestamp')}")
        st.write(f"💬 {msg.get('message')}")
        st.divider()

new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意") and new_msg:
    add_to_diary(new_msg)

# --- 4. 隱藏版管理員後台 ---
if st.query_params.get("admin") == "true":
    st.sidebar.divider()
    st.sidebar.subheader("👑 管理員專區")
    admin_input = st.sidebar.text_input("輸入管理員密鑰", type="password")
    if admin_input and admin_input == st.secrets.get("ADMIN_PASSWORD", ""):
        if st.sidebar.checkbox("查看登入紀錄"):
            st.sidebar.table(supabase.table("auth_log").select("*").execute().data)
