import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 設定 AI API
# 請確保你在 Streamlit Cloud 的 Secrets 設定了 API_KEY
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"API 設定錯誤，請檢查 Secrets: {e}")
    st.stop()

st.title("🐱 咪姐的秘密心聲")
st.write("上傳一張咪姐的照片，讓 AI 翻譯牠現在在想什麼！")

# 2. 上傳照片
uploaded_file = st.file_uploader("給 AI 看一張咪姐的照片 (JPG/PNG)", type=["jpg", "png"])

if uploaded_file is not None:
    try:
        # 將圖片轉為 RGB 格式，這是為了確保 AI 能穩定讀取
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="正在觀察咪姐...", use_column_width=True)
        
        # 3. 按下按鈕後，開始分析
        if st.button("翻譯咪姐的心聲"):
            with st.spinner('咪姐正在思考中...'):
                prompt = "這是一張貓咪的照片。請用可愛、有點傲嬌的口吻，描述這隻貓咪現在的心情或是在做什麼。"
                
                # 呼叫 AI
                response = model.generate_content([prompt, image])
                
                st.write("### 💬 咪姐說：")
                st.write(response.text)
    except Exception as e:
        st.error(f"圖片處理失敗，請試試看較小的檔案: {e}")
