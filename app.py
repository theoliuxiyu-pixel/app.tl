import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from datetime import datetime, timedelta

# API 設定
genai.configure(api_key=st.secrets["API_KEY"], transport='rest')
model = genai.GenerativeModel("gemini-3.5-flash")

st.title("🐱 咪姐的秘密心聲與加密日記")

# --- 1. AI 分析區塊 ---
uploaded_file = st.file_uploader("給 AI 看一張咪姐的照片", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((1024, 1024))
    st.image(image, caption="咪姐觀察中...", width=300)
    if st.button("翻譯咪姐心聲"):
        response = model.generate_content(["請用傲嬌口吻描述這隻貓咪現在的心情。", image])
        st.write(f"### 💬 咪姐說：\n{response.text}")

st.divider()

# --- 2. 加密留言板與圖片日記 ---
st.subheader("🔒 咪姐的加密罐罐日記")

# 設定密碼 (這裡範例設定為 1234，你可以隨意更改)
PASSWORD = "I_love_Mimi"
user_password = st.text_input("請輸入查看密碼：", type="password")

if user_password == PASSWORD:
    st.success("密碼正確，歡迎進入咪姐的秘密基地！")
    
    # 留言功能
    new_msg = st.text_input("想對咪姐說什麼？")
    # 留言圖片上傳
    msg_img = st.file_uploader("也可以附上一張紀錄照：", type=["jpg", "png"])
    
    if st.button("送出留言"):
        taiwan_time = datetime.now() + timedelta(hours=8)
        now = taiwan_time.strftime("%m/%d %H:%M")
        
        # 處理圖片保存
        img_filename = "none"
        if msg_img:
            img_filename = f"msg_{int(datetime.now().timestamp())}.jpg"
            msg_img_data = Image.open(msg_img)
            msg_img_data.save(img_filename)
            
        with open("diary.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{now}] 粉絲說: {new_msg} (圖片: {img_filename})")
        st.rerun()

    # 顯示歷史紀錄
    if os.path.exists("diary.txt"):
        with open("diary.txt", "r", encoding="utf-8") as f:
            st.text_area("歷史紀錄", value=f.read(), height=200, disabled=True)
else:
    st.warning("請輸入正確密碼以查看與留言。")
