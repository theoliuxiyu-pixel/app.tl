import streamlit as st
import google.generativeai as genai
from supabase import create_client
from datetime import datetime, timedelta

# --- 0. 初始化設定 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

def get_tw_date(): return (datetime.utcnow() + timedelta(hours=8)).date()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.last_login_date = None

# --- 1. 認證檢查 ---
def check_auth():
    if not st.session_state.authenticated: return False
    if st.session_state.last_login_date != get_tw_date():
        st.session_state.authenticated = False
        return False
    return True

if not check_auth():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼", type="password")
    if st.button("解鎖"):
        if password == "71398426":
            st.session_state.authenticated = True
            st.session_state.last_login_date = get_tw_date()
            st.rerun()
        else: st.error("密碼錯誤")
    st.stop()

# --- 2. 核心功能 ---
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 從資料庫計算好感度 (留言數)
def get_loyalty_score():
    try:
        data = supabase.table("diary").select("id", count='exact').execute()
        return data.count if data.count else 0
    except: return 0

score = get_loyalty_score()

# --- 3. 頁面顯示 ---
st.title("🐱 咪姐的永久秘密基地")
st.write(f"目前與咪姐的好感度：**{score}** 點")

# 圖片翻譯
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file:
    if st.button("翻譯咪姐心聲"):
        tone = "溫柔且親暱" if score >= 15 else ("傲嬌但有點害羞" if score >= 6 else "極度傲嬌、毒舌")
        prompt = f"你是一隻貓咪咪姐，好感度{score}。用{tone}口吻描述照片。格式：【傲嬌指數】：X/10 \n【翻譯心聲】：(描述)"
        try:
            # 簡化處理，直接讀取檔案串流
            response = model.generate_content([prompt, uploaded_file.getvalue()])
            st.write(f"### 💬 咪姐說：\n{response.text}")
        except: st.warning("咪姐現在不想理人。")

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
