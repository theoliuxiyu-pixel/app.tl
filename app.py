import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# 設定 API Keys (記得去 Streamlit Secrets 新增 TAVILY_API_KEY)
genai.configure(api_key=st.secrets["API_KEY"])
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🌐 即時毒舌科技情報站")
user_input = st.text_input("你想查哪款最新產品的評價？", "例如：Vision Pro 最新評價")

if st.button("開始即時分析"):
    with st.spinner('正在全網搜集毒舌素材...'):
        # 1. 聯網搜尋
        search_result = tavily.search(query=user_input, search_depth="advanced")
        context = "\n".join([result['content'] for result in search_result['results']])
        
        # 2. 讓 AI 根據搜尋結果評論
        prompt = f"""
        你是一位毒舌科技評論員。請根據以下最新的搜尋結果，犀利且幽默地分析該產品：
        搜尋到的最新資訊：
        {context}
        """
        response = model.generate_content(prompt)
        st.write(response.text)
