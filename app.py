import streamlit as st
import os
import random
from database import add_to_diary, get_recent_logs
from ai_engine import get_ai_response, optimize_image, create_mimi_icon
from auth import check_auth, set_auth

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

# --- 1. 登入邏輯 ---
if not check_auth():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("密碼", type="password")
    if st.button("解鎖"):
        if password == st.secrets.get("LOGIN_PASSWORD"):
            set_auth(True); st.rerun()
        else: st.error("密碼錯誤！")
    st.stop()

# --- 2. 主介面 ---
st.title("🐱 咪姐的秘密基地")
if st.sidebar.button("登出"):
    set_auth(False); st.rerun()

# 顯示 Icon
if os.path.exists("mimi_icon.png"): st.image("mimi_icon.png", width=150)

# --- 3. 猜拳遊戲區 ---
with st.expander("🥊 挑戰咪姐猜拳"):
    options = ["剪刀", "石頭", "布"]
    user_choice = st.radio("你出什麼？", options, horizontal=True)
    if st.button("確認出拳"):
        mi_choice = random.choice(options)
        st.write(f"咪姐出了：**{mi_choice}**")
        if (user_choice == "剪刀" and mi_choice == "布") or (user_choice == "石頭" and mi_choice == "剪刀") or (user_choice == "布" and mi_choice == "石頭"):
            st.success("🎉 贏了！好感度+1")
            add_to_diary("在猜拳中贏過了咪姐")
        elif user_choice == mi_choice: st.info("平手！")
        else: st.error("嗚嗚，咪姐贏了！")

# --- 4. 拍照與上傳區 ---
st.subheader("📸 拍給咪姐看")
uploaded_file = st.file_uploader("選擇照片", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    if col1.button("通靈這張照片"):
        with st.spinner("咪姐感應中..."):
            img_data = optimize_image(uploaded_file)
            st.write(f"🐱 咪姐說：{get_ai_response('評價這張照片', img_data)}")
            add_to_diary("上傳照片並進行了通靈")
    
    if col2.button("設為基地 Icon"):
        create_mimi_icon(uploaded_file)
        st.success("Icon 已更新！(請重新整理頁面)"); st.rerun()

# --- 5. 日記區 ---
st.subheader("📝 罐罐日記")
for log in get_recent_logs():
    st.write(f"[{log['timestamp']}] {log['message']}")
