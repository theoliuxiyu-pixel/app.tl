import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 設定 API
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🐱 咪姐的秘密心聲")

uploaded_file = st.file_uploader("上傳一張咪姐的照片 (建議 1MB 以下)", type=["jpg", "png"])

if uploaded_file is not None:
    # 讀取圖片並處理
    image = Image.open(uploaded_file)
    
    # 【關鍵步驟】：調整圖片大小以降低 API 壓力，防止 Timeout
    image.thumbnail((1024, 1024)) 
    
    st.image(image, caption="咪姐準備中...", width=400)
    
    if st.button("翻譯咪姐的心聲"):
        with st.spinner('咪姐正在靈魂溝通中...'):
            try:
                prompt = "你是一位貓咪翻譯官，請用傲嬌又可愛的口吻，猜猜這隻貓咪現在在想什麼。"
                # 傳送處理過的圖片物件給 AI
                response = model.generate_content([prompt, image])
                st.write("### 💬 咪姐說：")
                st.write(response.text)
            except Exception as e:
                st.error(f"分析失敗，這可能是因為網路連線中斷，請重按一次按鈕。錯誤碼: {e}")
