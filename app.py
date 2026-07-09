import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
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
        if password == "7139826":
            st.session_state.authenticated = True
            st.session_state.last_login_date = get_tw_date()
            st.rerun()
        else: st.error("密碼錯誤")
    st.stop()

# --- 2. 核心功能與資料庫 ---
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def get_loyalty_score():
    try:
        data = supabase.table("diary").select("id", count='exact').execute()
        return data.count if data.count else 0
    except: return 0

score = get_loyalty_score()

# --- 3. UI 美化與風格 (對比度優化) ---
def apply_theme(s):
    if s < 6: bg, txt, btn = "#f0f0f0", "#212529", "#333333"
    elif s < 15: bg, txt, btn = "#faedcd", "#5f4339", "#d4a373"
    else: bg, txt, btn = "#ffebf0", "#880e4f", "#ffafcc"
        
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg}; color: {txt}; }}
        h1, h2, h3, p, label, .stMarkdown, .stText {{ color: {txt} !important; }}
        div.stButton > button {{ background-color: {btn} !important; color: white !important; border: none; }}
        div[data-testid="stFileUploadDropzone"] {{ border: 2px dashed {txt} !important; background: rgba(255,255,255,0.2); }}
        input {{ border: 1px solid {txt} !important; }}
        </style>
    """, unsafe_allow_html=True)

apply_theme(score)

# --- 4. 頁面內容 ---
st.title("🐱 咪姐的永久秘密基地")
st.write(f"與咪姐的好感度：**{score}** 點")

uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        tone = "溫柔且親暱" if score >= 15 else ("傲嬌但有點害羞" if score >= 6 else "極度傲嬌、毒舌")
        prompt = f"你是一隻貓咪咪姐，好感度{score}。用{tone}口吻描述照片心情。格式：【傲嬌指數】：X/10 \n【翻譯心聲】：(描述)"
        try:
            response = model.generate_content([prompt, image])
            st.write(f"### 💬 咪姐說：\n{response.text}")
        except: st.warning("咪姐現在不想理人。")

st.divider()
st.subheader("📝 罐罐日記")
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        supabase.table("diary").insert({"timestamp": datetime.now().strftime("%m/%d %H:%M"), "message": new_msg}).execute()
        st.rerun()

data = supabase.table("diary").select("*").order("id", desc=True).execute().data
for msg in data: st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
