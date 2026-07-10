# app.py
import streamlit as st
from database import add_to_diary, get_recent_logs
from ai_engine import get_ai_response
from auth import check_auth, set_auth

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

# 登入邏輯
if not check_auth():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("密碼", type="password")
    if st.button("解鎖"):
        if password == st.secrets.get("LOGIN_PASSWORD"):
            set_auth(True)
            st.rerun()
        else: st.error("錯誤！")
    st.stop()

# 主介面
st.title("🐱 咪姐的秘密基地")
if st.button("登出"):
    set_auth(False)
    st.rerun()

# 拍照與通靈
img_file = st.camera_input("拍一張照給咪姐")
if img_file and st.button("讓咪姐通靈這張照片"):
    img_data = {"mime_type": "image/jpeg", "data": img_file.getvalue()}
    res = get_ai_response("看看這張照片，給點評價。", img_data)
    st.write(f"咪姐說：{res}")

# 日記區
st.subheader("📝 罐罐日記")
for log in get_recent_logs():
    st.write(f"{log['timestamp']}: {log['message']}")
