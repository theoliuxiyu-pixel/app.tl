import streamlit as st
import google.generativeai as genai
from PIL import Image
from supabase import create_client
from datetime import datetime, timedelta

# --- 1. 初始化設定 ---
# 確保你在 Streamlit Cloud 的 Secrets 設定了這些變數
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
st.title("🐱 咪姐的永久秘密基地")

# --- 2. AI 翻譯區塊 ---
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="正在觀察咪姐...", use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        with st.spinner('咪姐正在靈魂溝通中...'):
            response = model.generate_content(["請用傲嬌口吻描述這隻貓咪現在的心情。", image])
            st.write(f"### 💬 翻譯官：咪姐說：\n{response.text}")

st.divider()

# --- 3. 永久留言板 (Supabase) ---
st.subheader("📝 罐罐日記")

# 讀取資料庫中的所有留言
response = supabase.table("diary").select("*").order("id", desc=True).execute()
messages = response.data

for msg in messages:
    st.write(f"**{msg['timestamp']}**: {msg['message']}")

# 新增留言功能
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        taiwan_time = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        
        # 寫入 Supabase 資料庫
        supabase.table("diary").insert({
            "timestamp": taiwan_time, 
            "message": new_msg
        }).execute()
        
        # 重新整理顯示新留言
        st.rerun()
