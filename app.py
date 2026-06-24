import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from datetime import datetime

# 1. API 設定 (請確保 Streamlit Secrets 有 API_KEY)
# 使用 'rest' 傳輸方式以解決潛在的連線權限問題
genai.configure(api_key=st.secrets["API_KEY"], transport='rest')
model = genai.GenerativeModel("gemini-3.5-flash")

st.title("🐱 咪姐的秘密心聲與罐罐日記")

# 2. 圖片 AI 分析區塊
uploaded_file = st.file_uploader("請上傳一張咪姐的照片", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 影像處理與轉檔
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((1024, 1024))
    st.image(image, caption="正在觀察咪姐...", width=400)
    
    if st.button("翻譯咪姐的心聲"):
        with st.spinner('咪姐正在靈魂溝通中...'):
            try:
                prompt = "你是一位貓咪翻譯官，請用傲嬌、可愛且略帶調皮的口吻，描述這隻貓咪現在的行為或心情。"
                response = model.generate_content([prompt, image])
                st.write("### 💬 咪姐說：")
                st.write(response.text)
            except Exception as e:
                st.error(f"分析失敗: {e}")

# 3. 留言板/罐罐日記區塊
st.divider() 
st.subheader("📝 咪姐的專屬罐罐日記")

# 確保檔案存在，不存在就先建立
if not os.path.exists("diary.txt"):
    with open("diary.txt", "w", encoding="utf-8") as f:
        f.write("--- 咪姐的日記本開始囉 ---")

# 讀取並顯示日記
with open("diary.txt", "r", encoding="utf-8") as f:
    messages = f.read()

st.text_area("歷史紀錄", value=messages, height=150, disabled=True)

# 新增日記功能
new_msg = st.text_input("你想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        # 取得當前時間戳
        now = datetime.now().strftime("%m/%d %H:%M")
        
        # 追加寫入內容
        with open("diary.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{now}] 粉絲說: {new_msg}")
        
        # 重新整理讓留言立即顯示
        st.rerun()
