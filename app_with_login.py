import streamlit as st
from streamlit_oauth import OAuth2Component
import requests

# Google OAuth 設定
CLIENT_ID = "308161352982-u2jhji1lcqqb42o7oql0me3nat6l3efp.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://kpi-checker-junasnlqjy9vnrtp58g2xv.streamlit.app/"
SCOPE = "email profile openid"

# 建立 OAuth 元件
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    redirect_uri=REDIRECT_URI,
    scopes=[SCOPE]
)

# ✅ 設定白名單（可用 Gmail）
ALLOWED_USERS = [
    "ainstaccc@gmail.com",
    "ray@mistore.com.tw",
    "iven@mistore.com.tw",
    "guangan@mistore.com.tw",
    "wanju@mistore.com.tw",
    "hsiao@mistore.com.tw",
    "jc@mistore.com.tw",
    "keanu@mistore.com.tw",
    "katie@mistore.com.tw",
    "sisi@mistore.com.tw",
    "lizh@mistore.com.tw",
    "jen@mistore.com.tw",
    "mei@mistore.com.tw",
    "annie@mistore.com.tw",
    "ming@mistore.com.tw",
    "ting@mistore.com.tw",
    "cherry@mistore.com.tw",
    "vivian@mistore.com.tw",
    "amy@mistore.com.tw",
    "ivy@mistore.com.tw",
    "linda@mistore.com.tw",
    "vivi@mistore.com.tw"
]


# 取得使用者 email
def get_user_email(token):
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers).json()
        return user_info.get("email", "")
    return ""

# --- 登入流程 ---
st.title("📋 米斯特 門市 工作績效月考核查詢系統")

token = oauth2.authorize_button("🔐 使用 Google 帳號登入")

if token:
    user_email = get_user_email(token)
    st.success(f"✅ 登入成功：{user_email}")

    if user_email not in ALLOWED_USERS:
        st.error("❌ 此帳號未被授權使用本系統")
        st.stop()

    # ✅ 登入成功＆白名單通過後，顯示主畫面內容
    st.markdown("### 📊 米斯特 門市 工作績效月考核查詢系統")
    st.write("這裡可以顯示你原本的查詢模組、考核總表、人效分析、考核項目明細等主畫面內容。")

else:
    st.info("請先登入以使用本系統。")
