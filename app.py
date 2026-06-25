import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime, timedelta
import gspread

# 1. API 設定
genai.configure(api_key=st.secrets["API_KEY"], transport='rest')
model = genai.GenerativeModel("gemini-3.5-flash")

st.title("🐱 咪姐的永久秘密基地")

# 2. 連線 Google Sheet (使用公開連結的權限)
# 你需要先下載 gspread 的認證連結，或者直接改用此處邏輯：
# 為了簡化，建議你直接在 Streamlit secrets 裡放入你的 Google Sheet 名稱或網址
client = gspread.service_account(filename="service_account.json") 
sheet = client.open("咪姐日記").sheet1

# --- AI 分析區塊 ---
uploaded_file = st.file_uploader("上傳咪姐照片", type=["jpg", "png", "jpeg"])
if uploaded_file and st.button("翻譯心聲"):
    image = Image.open(uploaded_file).convert("RGB")
    response = model.generate_content(["傲嬌口吻描述這隻貓的心情", image])
    st.write(f"### 💬 翻譯官：咪姐說：\n{response.text}")

st.divider()

# --- 永久儲存留言區塊 ---
st.subheader("📝 咪姐日記")

# 顯示歷史留言
for row in sheet.get_all_records():
    st.text(f"[{row['Timestamp']}] {row['Message']}")

new_msg = st.text_input("想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        time_str = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        sheet.append_row([time_str, new_msg])
        st.rerun()
