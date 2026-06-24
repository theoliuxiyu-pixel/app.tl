import streamlit as st
import google.generativeai as genai

st.title("模型權限檢查器")

genai.configure(api_key=st.secrets["API_KEY"])

if st.button("查看我能用的模型"):
    # 這是最關鍵的一步：直接查詢所有可用的模型列表
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.write("你能使用的模型清單如下：")
    st.write(models)
    st.write("請將這個清單複製給我，我會告訴你該填入哪個名稱！")
