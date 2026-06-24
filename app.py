import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 設定 AI (記得要把 API_KEY 設定在 Streamlit Secrets 喔！)
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🐱 咪姐的秘密心聲")

# 2. 上傳照片
uploaded_file = st.file_uploader("給 AI 看一張咪姐的照片", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="正在觀察咪姐...", use_column_width=True)
    
    # 3. 按下按鈕後，讓 AI 講話
    if st.button("翻譯咪姐的心聲"):
        with st.spinner('咪姐翻譯官正在思考中...'):
            # 準備給 AI 的提示詞
            prompt = "這是一張我養的貓咪的照片。請你用可愛、有點傲嬌的貓咪口吻，描述牠現在的心情或是在做什麼。"
            
            # 把圖片和文字同時傳給 AI
            response = model.generate_content([prompt, image])
            
            st.write("### 💬 翻譯官：我覺得咪姐說：")
            st.write(response.text)
