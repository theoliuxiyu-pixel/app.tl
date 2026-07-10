import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageOps, ImageDraw
import io

genai.configure(api_key=st.secrets["API_KEY"])

def get_ai_response(prompt, img_bytes=None, current_score=0):
    # 根據分數動態調整傲嬌口吻
    mood = "你非常傲嬌，口氣冷淡，還會吐槽主人" if current_score < 10 else "你對主人開始信任了，語氣有些關心，但仍維持貓咪的尊嚴"
    model = genai.GenerativeModel("gemini-1.5-flash")
    system_prompt = f"你是咪姐，性格設定：{mood}。請用這種口吻回應。"
    
    content = [system_prompt + " " + prompt]
    if img_bytes: content.append({"mime_type": "image/jpeg", "data": img_bytes})
    return model.generate_content(content).text

def optimize_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    img.thumbnail((1024, 1024))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()

def create_mimi_icon(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    size = min(img.size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    output = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save("mimi_icon.png", "PNG")
