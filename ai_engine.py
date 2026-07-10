# ai_engine.py
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["API_KEY"])

def get_ai_response(prompt, img_bytes=None):
    model = genai.GenerativeModel("gemini-1.5-flash")
    system_prompt = "你是咪姐，一隻傲嬌但愛主人的貓。請用傲嬌、吐槽但帶點關心的口吻回應。"
    
    if img_bytes:
        response = model.generate_content([system_prompt + prompt, img_bytes])
    else:
        response = model.generate_content(system_prompt + prompt)
    return response.text
