import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# --- 1. 初始化設定 ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="咪姐秘密基地", page_icon="🐱")
st.title("🐱 咪姐的永久秘密基地")

# --- 2. 永久留言板區塊 ---
st.subheader("📝 罐罐日記")

# 嘗試讀取資料並顯示錯誤 (如果有)
try:
    response = supabase.table("diary").select("*").order("id", desc=True).execute()
    messages = response.data
    
    for msg in messages:
        st.text(f"[{msg.get('timestamp', '無時間')}] {msg.get('message', '無內容')}")
except Exception as e:
    st.error(f"讀取失敗: {e}")

# --- 3. 新增留言區塊 ---
new_msg = st.text_input("你想對咪姐說什麼？")
if st.button("獻上敬意"):
    if new_msg:
        taiwan_time = (datetime.now() + timedelta(hours=8)).strftime("%m/%d %H:%M")
        
        try:
            # 寫入資料庫
            supabase.table("diary").insert({
                "timestamp": taiwan_time, 
                "message": new_msg
            }).execute()
            
            st.success("留言成功！")
            st.rerun()
        except Exception as e:
            st.error(f"寫入失敗，請檢查權限或欄位: {e}")
    else:
        st.warning("請先輸入內容喔！")
