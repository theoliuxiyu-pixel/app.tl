import streamlit as st
import os
from database import add_to_diary, get_recent_logs
from ai_engine import get_ai_response, optimize_image, create_mimi_icon
from auth import check_auth, set_auth

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

if not check_auth():
    st.title("🔒 咪姐秘密基地")
    if st.text_input("密碼", type="password") == st.secrets.get("LOGIN_PASSWORD"):
        set_auth(True); st.rerun()
    st.stop()

st.title("🐱 咪姐的秘密基地")
if os.path.exists("mimi_icon.png"): st.image("mimi_icon.png", width=150)

uploaded_file = st.file_uploader("給咪姐看張照片", type=["jpg", "jpeg", "png"])
col1, col2 = st.columns(2)

if uploaded_file:
    if col1.button("通靈這張照片"):
        with st.spinner("咪姐感應中..."):
            img_data = optimize_image(uploaded_file)
            st.write(f"🐱 咪姐說：{get_ai_response('評價這張照片', img_data)}")
            add_to_diary("上傳照片並進行了通靈")
    
    if col2.button("設為基地 Icon"):
        create_mimi_icon(uploaded_file)
        st.success("Icon 已更新！(請重新整理頁面)"); st.rerun()

st.subheader("📝 罐罐日記")
for log in get_recent_logs(): st.write(f"[{log['timestamp']}] {log['message']}")
