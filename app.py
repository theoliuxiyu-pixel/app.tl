import streamlit as st
import google.generativeai as genai
import os

# 設定頁面標題
st.title("🤖 毒舌科技評論員")

# 1. 嘗試從 Streamlit Secrets 讀取，如果找不到則嘗試從環境變數讀取
try:
    if "API_KEY" in st.secrets:
        api_key = st.secrets["API_KEY"]
    else:
        api_key = os.environ.get("API_KEY")
        
    if not api_key:
        st.error("❌ 找不到 API_KEY！請檢查 Streamlit Cloud 的 Secrets 設定。")
        st.stop()
        
    genai.configure(api_key=api_key)
    # 不使用 list_models()，改為直接指定模型以提高穩定性
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"❌ 初始化錯誤: {e}")
    st.stop()

# 2. UI 介面
user_input = st.text_input("你想問什麼科技產品？", "例如：最新的折疊手機")

if st.button("開始毒舌分析"):
    with st.spinner('正在毒舌分析中...'):
        try:
            prompt = f"你是一位毒舌科技評論員，請用犀利、幽默的口吻分析：{user_input}"
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"生成內容時發生錯誤: {e}")
