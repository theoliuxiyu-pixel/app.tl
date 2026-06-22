import streamlit as st
import google.generativeai as genai
import os

# 1. 強制確認 Key 是否存在
if "API_KEY" not in st.secrets:
    st.error("找不到 API_KEY！請確認你有在 Streamlit Cloud 設定 Secrets。")
    st.stop()

# 2. 讀取並設定
api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)
# 自動獲取模型
def get_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

model = get_model()

st.title("🤖 毒舌科技評論員")
user_input = st.text_input("你想問什麼科技產品？", "例如：最新的折疊手機")

if st.button("開始毒舌分析"):
    if model:
        prompt = f"你是一位毒舌科技評論員，請用犀利、幽默的口吻分析：{user_input}"
        response = model.generate_content(prompt)
        st.write(response.text)
    else:
        st.write("找不到可用模型，請稍後再試。")
