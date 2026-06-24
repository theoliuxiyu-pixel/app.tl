import streamlit as st
from PIL import Image # 這是用來讀取圖片的工具

st.title("🐱 咪姐的專屬圖庫")

# 這裡就是 Scratch 的「詢問並等待」積木，只是換成了上傳檔案
uploaded_file = st.file_uploader("請上傳一張咪姐的照片", type=["jpg", "png"])

if uploaded_file is not None:
    # 把圖片顯示出來
    image = Image.open(uploaded_file)
    st.image(image, caption="這就是咪姐！", use_column_width=True)
    st.success("咪姐照片上傳成功！")
