import streamlit as st
import os
import random
from database import add_to_diary, get_recent_logs
from ai_engine import get_ai_response, optimize_image, create_mimi_icon
from auth import check_auth, set_auth

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

# 登入邏輯
if not check_auth():
    st.title("🔒 咪姐秘密基地")
    if st.text_input("密碼", type="password") == st.secrets.get("LOGIN_PASSWORD"):
        set_auth(True); st.rerun()
    st.stop()

# 頁面主體
st.title("🐱 咪姐的秘密基地")
if os.path.exists("mimi_icon.png"): st.image("mimi_icon.png", width=120)

# --- 猜拳 (移至主頁面，使用 Expander) ---
with st.expander("🥊 挑戰咪姐猜拳 (點擊展開)"):
    options = ["剪刀", "石頭", "布"]
    choice = st.radio("你出什麼？", options, horizontal=True)
    if st.button("確認出拳"):
        mi = random.choice(options)
        st.write(f"咪姐出了：**{mi}**")
        if (choice == "剪刀" and mi == "布") or (choice == "石頭" and mi == "剪刀") or (choice == "布" and mi == "石頭"):
            st.success("贏了！好感度+1"); add_to_diary("猜拳贏了咪姐")
        elif choice == mi: st.info("平手！")
        else: st.error("嗚嗚，咪姐贏了！")

# 拍照/上傳區
st.subheader("📸 拍給咪姐看")
file = st.file_uploader("選擇照片", type=["jpg", "png"])
if file:
    col1, col2 = st.columns(2)
    if col1.button("通靈"):
        with st.spinner("咪姐感應中..."):
            res = get_ai_response("評價這張照片", optimize_image(file))
            st.write(f"🐱 咪姐說：{res}"); add_to_diary("傳送了照片")
    if col2.button("設為基地 Icon"):
        create_mimi_icon(file); st.success("已更新！"); st.rerun()

# 日記區
st.subheader("📝 罐罐日記")
for log in get_recent_logs(): st.write(f"[{log['timestamp']}] {log['message']}")

if st.button("登出"): set_auth(False); st.rerun()
