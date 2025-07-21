import streamlit as st
from streamlit_oauth import OAuth2Component
import requests

# Google OAuth 設定
CLIENT_ID = "308161352982-u2jhji1lcqqb42o7oql0me3nat6l3efp.apps.googleusercontent.com"
CLIENT_SECRET = "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"

oauth = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    revoke_endpoint="https://oauth2.googleapis.com/revoke",
)

def get_user_email(token):
    """使用 access_token 查詢使用者 Email"""
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    if response.status_code == 200:
        return response.json().get("email", "unknown")
    else:
        return "unknown"

def main():
    st.title("🔐 米斯特 門市 工作績效月考核查詢系統 登入驗證")
    
    # 登入按鈕（點擊後導入 Google OAuth 流程）
    token = oauth.authorize_button(
        name="📧 使用 Google 帳號登入",
        redirect_uri="http://localhost:8501",
        scope=["https://www.googleapis.com/auth/userinfo.email"],
        key="google"
    )

    if token:
        user_email = get_user_email(token)
        st.success(f"✅ 登入成功：{user_email}")

        # 限制特定網域或帳號白名單（這邊只做範例）
        if not user_email.endswith("@gmail.com"):
            st.error("❌ 此帳號無授權使用本系統")
            st.stop()

        # 登入後的主畫面功能
        st.markdown("### 🎯 查詢畫面主頁（登入後才可見）")
        st.write("這裡可以放入你的查詢模組與數據展示功能")

    else:
        st.warning("⚠️ 尚未登入，請先使用 Google 帳號登入")
        st.stop()

if __name__ == "__main__":
    main()
