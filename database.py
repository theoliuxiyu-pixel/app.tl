import streamlit as st
from supabase import create_client
from datetime import datetime, timezone, timedelta

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def log_interaction(message, score_delta):
    """記錄對話並儲存好感度分數"""
    try:
        supabase.table("mood_log").insert({
            "timestamp": datetime.now(timezone(timedelta(hours=8))).strftime("%m/%d %H:%M"),
            "mood_score": score_delta,
            "message": message
        }).execute()
        return True
    except: return False

def get_total_mood_score():
    """統計所有互動得分"""
    try:
        logs = supabase.table("mood_log").select("mood_score").execute().data
        return sum(log['mood_score'] for log in logs) if logs else 0
    except: return 0

def add_to_diary(message):
    supabase.table("diary").insert({"timestamp": datetime.now(timezone(timedelta(hours=8))).strftime("%m/%d %H:%M"), "message": message}).execute()

def get_recent_logs():
    return supabase.table("diary").select("*").order("id", desc=True).limit(10).execute().data
