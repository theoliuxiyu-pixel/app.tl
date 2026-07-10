import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageOps, ImageDraw
import io

genai.configure(api_key=st.secrets["API_KEY"])

# 處理上傳給 AI 的照片 (壓縮)
def optimize_image(uploaded_file):
    img = Image.open(uploaded_file)
    img.thumbnail((1000, 1000))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()

# 製作圓形 Icon 的功能
def create_mimi_icon(uploaded_file, output_path="mimi_icon.png"):
    img = Image.open(uploaded_file).convert("RGB")
    size = min(img.size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    output = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save(output_path, "PNG")

def get_ai_response(prompt, img_bytes=None):
    model = genai.GenerativeModel("gemini-3.5-flash")
    system_prompt = "你是咪姐，傲嬌貓咪。用傲嬌口吻評論。"
    content = [system_prompt + prompt]
    if img_bytes:
        content.append({"mime_type": "image/jpeg", "data": img_bytes})
    return model.generate_content(content).text
