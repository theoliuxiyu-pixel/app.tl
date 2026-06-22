import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# 設定 API
genai.configure(api_key=st.secrets["API_KEY"])
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🌐 AI 科技評論情報站")

# 1. 新增選擇功能
persona = st.selectbox(
    "選擇你的評論員風格：",
    ("毒舌評論員", "溫柔分析師", "專業硬核工程師")
)

user_input = st.text_input("你想查哪款最新產品的評價？", "例如：Vision Pro 最新評價")

# 2. 定義不同風格的指令
system_prompts = {
    "毒舌評論員": "你是一位毒舌科技評論員，分析要犀利、幽默、充滿嘲諷，直擊產品缺點。",
    "溫柔分析師": "你是一位溫柔客觀的分析師，你會照顧使用者的感受，平衡分析產品的優缺點，給出中肯建議。",
    "專業硬核工程師": "你是一位專業的硬核工程師，專注於硬體規格、架構與技術細節，用詞嚴謹、數據化，不講廢話。"
}

if st.button("開始分析"):
    with st.spinner('正在全網搜集素材...'):
        # 聯網搜尋
        search_result = tavily.search(query=user_input, search_depth="advanced")
        context = "\n".join([result['content'] for result in search_result['results']])
        
        # 根據選擇的風格組合 prompt
        prompt = f"""
        {system_prompts[persona]}
        請根據以下最新的搜尋結果，分析該產品：
        {context}
        """
        
        response = model.generate_content(prompt)
        st.write(f"### 🧐 {persona} 的觀點：")
        st.write(response.text)
