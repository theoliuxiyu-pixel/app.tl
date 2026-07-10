import streamlit as st
import google.generativeai as genai
import requests
from supabase import create_client
from datetime import datetime, timedelta

# --- 0. 設定 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])

# 取得使用者真實 IP
def get_user_ip():
    try:
        # 使用公開 API 取得 IP
        return requests.get('https://api.ipify.org').text
    except:
        return "unknown"

user_ip = get_user_ip()

# --- 1. 冷卻檢查邏輯 (基於 IP) ---
def check_supabase_auth():
    # 查詢該 IP 的狀態
    res = supabase.table("auth_log").select("status, last_attempt_time").eq("session_id", user_ip).execute()
    
    if len(res.data) > 0:
        row = res.data[0]
        # 如果已經解鎖過
        if row['status'] == True:
            return True
        
        # 檢查是否在 10 分鐘冷卻內
        if row['last_attempt_time']:
            # 解析資料庫時間
            last_time = datetime.fromisoformat(row['last_attempt_time'].replace('Z', '+00:00'))
            # 轉換為本地時間比對
            if datetime.now(last_time.tzinfo) - last_time < timedelta(minutes=10):
                st.error(f"❌ 偵測到多次失敗嘗試，IP: {user_ip} 暫時鎖定 10 分鐘。")
                st.stop()
    return False

# --- 2. 登入介面 ---
if not check_supabase_auth():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼", type="password")
    
    if st.button("解鎖"):
        if password == "71398426":
            # 成功：清除冷卻狀態
            supabase.table("auth_log").upsert({
                "session_id": user_ip,
                "status": True,
                "last_attempt_time": None
            }).execute()
            st.rerun()
        else:
            # 失敗：記錄當前時間
            supabase.table("auth_log").upsert({
                "session_id": user_ip,
                "status": False,
                "last_attempt_time": datetime.now().isoformat()
            }).execute()
            st.error("密碼錯誤，若連續錯誤將觸發 10 分鐘保護機制。")
            st.stop()

# --- 3. 核心功能 ---
st.title("🐱 咪姐的永久秘密基地")
model = genai.GenerativeModel("gemini-1.5-flash")

# 計算好感度
try:
    score = supabase.table("diary").select("id", count='exact').execute().count or 0
    st.write(f"目前與咪姐的好感度：**{score}** 點")
except:
    score = 0

# 功能區 (拍照、日記)
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file and st.button("翻譯咪姐心聲"):
    prompt = f"你是一隻貓咪咪姐，好感度{score}，用傲嬌口吻描述照片。"
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
