import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageOps, ImageDraw
import io

# 設定 API 金鑰
genai.configure(api_key=st.secrets["API_KEY"])

def get_best_model():
    """自動偵測並回傳目前帳號可用的 Gemini 模型名稱"""
    try:
        # 列出所有支援內容生成的模型
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 優先權排序
        priorities = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        for p in priorities:
            if p in models:
                return p
        return models[0] if models else "gemini-1.5-flash"
    except Exception:
        return "gemini-1.5-flash"

def optimize_image(uploaded_file):
    """將圖片壓縮至合適的大小，減少 API 傳輸耗損"""
    try:
        img = Image.open(uploaded_file).convert("RGB")
        img.thumbnail((1024, 1024)) # 限制最大邊長
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"圖片處理錯誤: {e}")
        return None

def create_mimi_icon(uploaded_file, output_path="mimi_icon.png"):
    """將圖片裁切成圓形並儲存為 Icon"""
    try:
        img = Image.open(uploaded_file).convert("RGB")
        size = min(img.size)
        
        # 製作圓形遮罩
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # 裁切並套用
        output = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(output_path, "PNG")
    except Exception as e:
        st.error(f"Icon 製作失敗: {e}")

def get_ai_response(prompt, img_bytes=None):
    """呼叫 AI 模型進行通靈回應"""
    try:
        model_name = get_best_model()
        model = genai.GenerativeModel(model_name=model_name)
        
        system_prompt = "你是咪姐，一隻傲嬌但愛主人的貓。請用傲嬌、吐槽但帶點關心的口吻回應。"
        content = [system_prompt + " " + prompt]
        
        if img_bytes:
            content.append({"mime_type": "image/jpeg", "data": img_bytes})
            
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"咪姐通靈失敗了... (錯誤訊息: {str(e)[:50]})"
