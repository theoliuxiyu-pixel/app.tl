import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 強制設定 API 傳輸方式為 'rest'，這是解決 404 錯誤的關鍵
genai.configure(api_key=st.secrets["API_KEY"], transport='rest')

# 2. 使用更直接的模型名稱宣告
# 我們嘗試使用 'gemini-1.5-flash'，這是目前最推薦的視覺模型
try:
    model = model = genai.GenerativeModel("gemini-pro") 
except Exception as e:
    st.error(f"模型載入失敗: {e}")

st.title("🐱 咪姐的秘密心聲")

# 3. 圖片上傳區塊
uploaded_file = st.file_uploader("請上傳一張咪姐的照片", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 讀取並轉為 RGB
    image = Image.open(uploaded_file).convert("RGB")
    
    # 將圖片縮小以防傳輸超時
    image.thumbnail((1024, 1024))
    
    st.image(image, caption="正在觀察咪姐...", width=400)
    
    if st.button("翻譯咪姐的心聲"):
        with st.spinner('咪姐正在靈魂溝通中...'):
            try:
                # 4. 生成內容
                prompt = "你是一位貓咪翻譯官，請用傲嬌、可愛且略帶調皮的口吻，描述這隻貓咪現在的行為或心情。"
                response = model.generate_content([prompt, image])
                
                st.write("### 💬 咪姐說：")
                st.write(response.text)
            except Exception as e:
                # 如果這裡又報錯，錯誤訊息會顯示在網頁上，請把它複製給我
                st.error(f"分析失敗: {e}")
                st.write("如果是 404 錯誤，請確認你的 API Key 是否有權限使用 Gemini 1.5 系列模型。")
