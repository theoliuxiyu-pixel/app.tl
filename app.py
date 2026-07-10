import streamlit as st
import os, random
from database import add_to_diary, get_recent_logs, log_interaction, get_total_mood_score
from ai_engine import get_ai_response, optimize_image, create_mimi_icon
from auth import check_auth, set_auth
from weather import get_weather_commentary

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")

# 登入邏輯
if not check_auth():
    st.title("🔒 咪姐秘密基地")
    password = st.text_input("密碼", type="password")
    remember = st.checkbox("保持登入狀態", value=True)
    if st.button("進入基地"):
        if password == st.secrets.get("LOGIN_PASSWORD"):
            set_auth(True, remember_me=remember); st.rerun()
        else: st.error("密碼錯誤，咪姐不想理你。")
    st.stop()

# 主頁面
st.title("🐱 咪姐的秘密基地")
current_score = get_total_mood_score()
st.metric("咪姐好感度", current_score)

if os.path.exists("mimi_icon.png"): st.image("mimi_icon.png", width=120)

with st.expander("🌤️ 咪姐的天氣建議"):
    if st.button("外面天氣如何？"):
        st.write(f"🐱 咪姐說：{get_weather_commentary()}")
        log_interaction("詢問天氣", 1)

with st.expander("🥊 挑戰咪姐猜拳"):
    choice = st.radio("你出什麼？", ["剪刀", "石頭", "布"], horizontal=True)
    if st.button("確認出拳"):
        mi = random.choice(["剪刀", "石頭", "布"])
        st.write(f"咪姐出了：**{mi}**")
        if (choice == "剪刀" and mi == "布") or (choice == "石頭" and mi == "剪刀") or (choice == "布" and mi == "石頭"):
            st.success("贏了！"); log_interaction("猜拳獲勝", 5)
        else: st.error("嗚嗚，咪姐贏了！"); log_interaction("猜拳輸了", 0)

st.subheader("📸 拍給咪姐看")
file = st.file_uploader("選擇照片", type=["jpg", "png"])
if file:
    col1, col2 = st.columns(2)
    if col1.button("通靈"):
        res = get_ai_response("評價這張照片", optimize_image(file), current_score)
        st.write(f"🐱 咪姐說：{res}"); log_interaction(res, 2); st.rerun()
    if col2.button("設為 Icon"): create_mimi_icon(file); st.rerun()

st.subheader("✍️ 寫點東西給咪姐")
text = st.text_area("今天發生了什麼事？")
if st.button("存入日記"): add_to_diary(text); st.rerun()

for log in get_recent_logs(): st.write(f"[{log['timestamp']}] {log['message']}")
if st.button("登出"): set_auth(False); st.rerun()
