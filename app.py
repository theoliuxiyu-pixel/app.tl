import streamlit as st
import google.generativeai as genai
from PIL import Image
from supabase import create_client
from datetime import datetime, timedelta

# --- 1. 設定頁面 ---
st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
st.title("🐱 咪姐的永久秘密基地")

# --- 2. 初始化服務 ---
# 確保你在 Streamlit Secrets 都有填入這些 Key
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel("gemini-3.5-flash")
except Exception as e:
    st.error("設定檔讀取失敗，請檢查 Streamlit Secrets 是否設定正確。")

# --- 3. AI 翻譯區塊 ---
st.subheader("📸 咪姐心情翻譯機")
uploaded_file = st.file_uploader("給咪姐拍張照", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="咪姐正在看你...", use_column_width=True)
    if st.button("翻譯咪姐心聲"):
        with st.spinner('Translating...'):
            try:
                response = model.generate_content(["請用傲嬌、愛理不理的口吻描述這隻貓咪現在的心情。", image])
                st.write(f"### 💬 翻譯官：咪姐說：\n{response.text}")
            except Exception as e:
                st.error(f"AI 翻譯暫時罷工了：{e}")

st.divider()

# --- 4. 永久留言板 (Supabase) ---
st.subheader("📝 罐罐日記")

# A. 顯示舊留言
try:
    response = supabase.table("diary").select("*").order("id", desc=True).execute()
    messages = response.data
    for msg in messages:
        st.write(f"**{msg.get('timestamp')}**: {msg.get('message')}")
except Exception as e:
    st.error(f"留言牆讀取失敗: {e}")

# B. 新增留言
new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        taiwan_time = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        try:
            # 注意：這裡只寫入 timestamp 和 message，id 會自動處理
            supabase.table("diary").insert({
                "timestamp": taiwan_time, 
                "message": new_msg
            }).execute()
            st.success("留言已送達咪姐的心裡！")
            st.rerun()
        except Exception as e:
            st.error(f"獻上敬意失敗：{e}")
    else:
        st.warning("你還沒說話呢，咪姐會生氣喔！")
