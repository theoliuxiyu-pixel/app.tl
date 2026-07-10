import streamlit as st
import google.generativeai as genai
from supabase import create_client
from datetime import datetime, timedelta

# --- 0. 設定 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# --- 1. 認證系統 (Supabase 後端驗證) ---
def get_tw_date_str(): 
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d")

# 產生唯一會話識別碼 (存於 session_state，網頁關閉即消失)
if "my_session" not in st.session_state:
    st.session_state.my_session = str(datetime.utcnow().timestamp())

def check_supabase_auth():
    today = get_tw_date_str()
    # 檢查該 session_id 是否在今天有解鎖紀錄
    res = supabase.table("auth_log").select("status").eq("unlock_date", today).eq("session_id", st.session_state.my_session).execute()
    return len(res.data) > 0 and res.data[0]['status'] == True

# --- 2. 登入介面 ---
if not check_supabase_auth():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("輸入密碼", type="password")
    if st.button("解鎖"):
        if password == "Meow123":
            # 寫入解鎖紀錄
            supabase.table("auth_log").insert({
                "unlock_date": get_tw_date_str(), 
                "status": True, 
                "session_id": st.session_state.my_session
            }).execute()
            st.rerun()
        else:
            st.error("密碼錯誤")
    st.stop()

# --- 3. 核心功能 ---
st.title("🐱 咪姐的永久秘密基地")

# 計算好感度
try:
    score = supabase.table("diary").select("id", count='exact').execute().count or 0
    st.write(f"目前與咪姐的好感度：**{score}** 點")
except:
    score = 0

# 圖片翻譯
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file and st.button("翻譯咪姐心聲"):
    tone = "溫柔且親暱" if score >= 15 else ("傲嬌但有點害羞" if score >= 6 else "極度傲嬌、毒舌")
    prompt = f"你是一隻貓咪咪姐，好感度{score}。用{tone}口吻描述照片。格式：【傲嬌指數】：X/10 \n【翻譯心聲】：(描述)"
    try:
        response = model.generate_content([prompt, uploaded_file.getvalue()])
        st.write(f"### 💬 咪姐說：\n{response.text}")
    except: 
        st.warning("咪姐現在不想理人。")

# 日記區
st.divider()
st.subheader("📝 罐罐日記")
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意") and new_msg:
    supabase.table("diary").insert({
        "timestamp": datetime.now().strftime("%m/%d %H:%M"), 
        "message": new_msg
    }).execute()
    st.rerun()

data = supabase.table("diary").select("*").order("id", desc=True).execute().data
for msg in data: 
    st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
