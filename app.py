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
    summary_month = df_summary.columns[0]  # 欄名是月份
    return df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month

df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

st.title("米斯特門市考核查詢平台")
st.markdown(f"## 查詢月份：{summary_month}")
st.markdown("### 查詢條件")
st.markdown("<span style='color:red'>請擇一條件進行查詢</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    q_mgr = st.text_input("區主管")
    q_dept = st.text_input("部門編號")
with col2:
    q_id = st.text_input("員工編號")
    q_name = st.text_input("姓名")

if st.button("查詢"):
    filled = [bool(q_mgr), bool(q_dept), bool(q_id), bool(q_name)]
    if sum(filled) != 1:
        st.error("❗請僅輸入一個查詢條件")
    else:
        def filter_df(df):
            if q_mgr: return df[df["區主管"] == q_mgr]
            if q_dept: return df[df["部門編號"] == q_dept]
            if q_id: return df[df["員編"] == q_id]
            if q_name: return df[df["人員姓名"].str.contains(q_name, na=False)]
            return df  # fallback

        for title, df in [("1️⃣ 門店考核總表", df_summary),
                          ("2️⃣ 人效分析", df_eff),
                          ("3️⃣ 店長副店 考核明細", df_mgr),
                          ("4️⃣ 店員儲備 考核明細", df_staff)]:
            st.subheader(title)
            result = filter_df(df)
            if result.empty:
                st.warning("⚠️ 查無資料")
            else:
                st.dataframe(result.round(1), use_container_width=True)

st.subheader("📊 本次考核等級分布")
st.dataframe(df_dist, use_container_width=True)
