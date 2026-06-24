import streamlit as st
from PIL import Image

st.title("測試：咪姐照片顯示器")
uploaded_file = st.file_uploader("測試上傳", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="成功讀取圖片！", use_column_width=True)
    st.write("如果看到這張圖，代表你的網頁環境是正常的。")
