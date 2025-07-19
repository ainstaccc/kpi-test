import streamlit as st

# 合法 Gmail 名單
AUTHORIZED_USERS = {
    "fabio89608@gmail.com": "李政勳",
    "124453221s@gmail.com": "鄧思思",
    "yolu902@gmail.com": "林宥儒",
    "a6108568@gmail.com": "羅婉心",
    "Wmksue12976@gmail.com": "王建樹",
    "aqianyu8@gmail.com": "楊茜聿",
    "happy0623091@gmail.com": "陳宥蓉",
    "cvcv0897@gmail.com": "吳岱侑",
    "minkatieweng@gmail.com": "翁聖閔",
    "a0956505289@gmail.com": "黃啟周",
    "Noncks@gmail.com": "栗晉屏",
    "vicecolife0969@gmail.com": "王瑞辰"
}

def check_login():
    st.subheader("登入驗證")
    email = st.text_input("請輸入您的 Gmail", placeholder="xxx@gmail.com")
    if st.button("登入"):
        if email in AUTHORIZED_USERS:
            st.success(f"登入成功，歡迎 {AUTHORIZED_USERS[email]}")
            return True
        else:
            st.error("無授權帳號，請洽管理部申請開通")
            return False
    return False
