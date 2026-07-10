# auth.py
import streamlit as st
from streamlit_cookies_controller import CookieController

cookies = CookieController()

def check_auth():
    return cookies.get("is_authenticated") == "True"

def set_auth(status=True):
    cookies.set("is_authenticated", "True" if status else "False", max_age=365*24*3600)
