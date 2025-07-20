import streamlit as st
import pandas as pd

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"

@st.cache_data(ttl=3600)
def load_data():
    xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
    df_summary = xls.parse("門店 考核總表", header=1)
    df_eff = xls.parse("人效分析", header=1)
    df_mgr = xls.parse("店長副店 考核明細", header=1)
    df_staff = xls.parse("店員儲備 考核明細", header=1)
    df_dist = xls.parse("等級分布", header=None, nrows=15, usecols="A:N")
    summary_month = xls.parse("門店 考核總表", nrows=1).columns[0]
    return df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month

st.set_page_config(page_title="米斯特 KPI 查詢平台", layout="wide")
st.markdown("<style>.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

st.title("📋 本月考核等級分布")
st.image("https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/dist.png", caption=f"{summary_month} 本月考核等級分布")

# 錯誤處理用 Try 包住 dataframe 顯示
try:
    st.dataframe(df_dist, use_container_width=True)
except Exception as e:
    st.error("資料表載入失敗，請稍後再試")
    st.code(str(e))

st.markdown("## 🔍 查詢")
with st.form("search_form"):
    col1, col2 = st.columns(2)
    with col1:
        staff_id = st.text_input("輸入員工編號")
    with col2:
        check_month = st.selectbox("選擇查詢月份", options=[summary_month])
    submitted = st.form_submit_button("🔎 查詢", type="primary")

    if submitted:
        result_mgr = df_mgr[df_mgr["員工編號"] == staff_id]
        result_staff = df_staff[df_staff["員工編號"] == staff_id]

        if not result_mgr.empty:
            st.success("查詢結果 - 店長／副店長")
            st.dataframe(result_mgr, use_container_width=True)
        elif not result_staff.empty:
            st.success("查詢結果 - 店員／儲備幹部")
            st.dataframe(result_staff, use_container_width=True)
        else:
            st.warning("⚠️ 查無此員工帳號，請確認員編是否正確。")
