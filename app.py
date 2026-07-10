import streamlit as st
import google.generativeai as genai
import requests
from supabase import create_client
from datetime import datetime, timedelta
# --- 修改這裡：修正導入名稱 ---
from streamlit_cookies_controller import CookieController 

# --- 0. 初始化 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
# --- 修改這裡：修正控制器名稱 ---
cookies = CookieController()

if "expiry_days" not in st.session_state:
    st.session_state.expiry_days = 30

def get_user_ip():
    try: return requests.get('https://api.ipify.org', timeout=2).text
    except: return "unknown"

# --- 1. 認證與冷卻系統 ---
def check_auth_and_cooldown():
    # --- 修改這裡：這裡也要確認是用 cookies.get ---
    if cookies.get("is_authenticated") == "True":
        return True
    
    user_ip = get_user_ip()
    res = supabase.table("auth_log").select("status, last_attempt_time").eq("session_id", user_ip).execute()
    
    if len(res.data) > 0:
        row = res.data[0]
        if row['status'] == True: return True
        if row['last_attempt_time']:
            last_time = datetime.fromisoformat(row['last_attempt_time'].replace('Z', '+00:00'))
            if datetime.now(last_time.tzinfo) - last_time < timedelta(minutes=10):
                st.error("❌ 嘗試次數過多，IP 已暫時冷卻 10 分鐘。")
                st.stop()
    return False

# --- 2. 登入介面 ---
if not check_auth_and_cooldown():
    st.title("🔒 咪姐秘密基地")
    st.session_state.expiry_days = st.number_input("設定記住我的天數：", min_value=1, max_value=365, value=st.session_state.expiry_days)
    password = st.text_input("輸入密碼", type="password")
    remember_me = st.checkbox(f"記住我 ({st.session_state.expiry_days}天內免登入)")
    
    if st.button("解鎖"):
        if password == "71398426":
            expiry = st.session_state.expiry_days if remember_me else None
            # --- 修改這裡：修正設定方式 ---
            cookies.set("is_authenticated", "True", max_age=expiry * 24 * 3600 if expiry else None)
            supabase.table("auth_log").upsert({"session_id": get_user_ip(), "status": True, "last_attempt_time": None}).execute()
            st.rerun()
        else:
            supabase.table("auth_log").upsert({"session_id": get_user_ip(), "status": False, "last_attempt_time": datetime.now().isoformat()}).execute()
            st.error("密碼錯誤！")
    st.stop()

# --- 3. 核心功能 ---
st.title("🐱 咪姐的永久秘密基地")

if st.button("登出"):
    cookies.remove("is_authenticated")
    st.rerun()

model = genai.GenerativeModel("gemini-1.5-flash")
score = supabase.table("diary").select("id", count='exact').execute().count or 0

if score >= 15: rank = "👑 咪姐的專屬奴才"
elif score >= 6: rank = "🐾 咪姐的朋友"
else: rank = "🐱 傲嬌路人"
st.write(f"目前與咪姐的好感度：**{score}** 點 | 階級：**{rank}**")

uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file and st.button("翻譯咪姐心聲"):
    prompt = f"你是一隻貓咪咪姐，好感度{score}，階級{rank}。用傲嬌口吻描述照片。"
    res = model.generate_content([prompt, uploaded_file.getvalue()])
    st.write(f"### 💬 咪姐說：\n{res.text}")

st.divider()
st.subheader("📝 罐罐日記")
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意") and new_msg:
    supabase.table("diary").insert({"timestamp": datetime.now().strftime("%m/%d %H:%M"), "message": new_msg}).execute()
    st.rerun()

for msg in supabase.table("diary").select("*").order("id", desc=True).execute().data:
    st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
