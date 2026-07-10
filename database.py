# database.py
from supabase import create_client
import streamlit as st
from datetime import datetime, timezone, timedelta

# 建立資料庫連線物件
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def add_to_diary(message):
    try:
        supabase.table("diary").insert({
            "timestamp": datetime.now(timezone(timedelta(hours=8))).strftime("%m/%d %H:%M"), 
            "message": message
        }).execute()
        return True
    except Exception as e:
        st.error(f"資料庫寫入失敗: {e}")
        return False

def get_recent_logs(limit=10):
    return supabase.table("diary").select("*").order("id", desc=True).limit(limit).execute().data
