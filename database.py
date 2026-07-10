import streamlit as st
from supabase import create_client
from datetime import datetime, timezone, timedelta

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def add_to_diary(message):
    try:
        supabase.table("diary").insert({
            "timestamp": datetime.now(timezone(timedelta(hours=8))).strftime("%m/%d %H:%M"), 
            "message": message
        }).execute()
        return True
    except: return False

def get_recent_logs(limit=10):
    return supabase.table("diary").select("*").order("id", desc=True).limit(limit).execute().data
