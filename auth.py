from streamlit_cookies_controller import CookieController

# 初始化時確保實例化正確
cookies = CookieController()

def check_auth():
    try:
        # 額外增加檢查，確保 cookies 屬性不為 None
        if hasattr(cookies, 'get'):
            return cookies.get("is_authenticated") == "True"
        return False
    except Exception:
        # 如果出錯，預設為未登入
        return False

def set_auth(status=True):
    try:
        cookies.set("is_authenticated", "True" if status else "False", max_age=365*24*3600)
    except Exception as e:
        print(f"Cookie 設定失敗: {e}")
