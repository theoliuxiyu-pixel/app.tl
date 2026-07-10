from streamlit_cookies_controller import CookieController
cookies = CookieController()

def check_auth():
    try:
        return cookies.get("is_authenticated") == "True"
    except: return False

def set_auth(status=True, remember_me=True):
    duration = 365*24*3600 if remember_me else 24*3600
    cookies.set("is_authenticated", "True" if status else "False", max_age=duration)
