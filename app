# 1. 安裝 Streamlit
!pip install -q streamlit

# 2. 寫入你的網頁程式碼
with open("app.py", "w") as f:
    f.write("""
import streamlit as st
import google.generativeai as genai

# 設定 AI
genai.configure(api_key="AQ.Ab8RN6J5kA9S5gPoKbjjiIG6eKNZ-kGR7HdGTvgjbPxuQ-PuFw")
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🤖 毒舌科技評論員")
user_input = st.text_input("你想問什麼科技產品？", "例如：最新的折疊手機")

if st.button("開始毒舌分析"):
    prompt = f"你是一位毒舌科技評論員，請用犀利、幽默的口吻分析：{user_input}"
    response = model.generate_content(prompt)
    st.write(response.text)
""")

# 3. 執行網頁 (在 Colab 裡我們使用 localtunnel 映射)
!npm install localtunnel
!streamlit run app.py &>/content/logs.txt &
!npx localtunnel --port 8501
