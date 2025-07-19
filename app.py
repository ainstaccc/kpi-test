
import streamlit as st
import pandas as pd

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"

@st.cache_data(ttl=3600)
def load_data():
    xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
    df_summary = xls.parse("門店 考核總表", header=1)
    df_dist = xls.parse("等級分布", header=None, nrows=15, usecols="A:N")
    summary_month = xls.parse("門店 考核總表", nrows=1).columns[0]
    return df_summary, df_dist, summary_month

df_summary, df_dist, summary_month = load_data()

st.title("📊 門市考核查詢系統")
st.subheader(f"🔎 查詢條件（{summary_month}）")
st.markdown("⚠ 區主管、部門編號、員工編號、姓名、查詢月份 擇一填寫即可，避免多重條件造成錯誤", unsafe_allow_html=True)

with st.form("search_form"):
    col1, col2 = st.columns(2)
    with col1:
        manager = st.text_input("區主管")
        dept_id = st.text_input("部門編號")
    with col2:
        emp_id = st.text_input("員工編號")
        name = st.text_input("姓名")

    query_month = summary_month

    submitted = st.form_submit_button("查詢")

if submitted:
    filtered_df = df_summary.copy()
    if manager:
        filtered_df = filtered_df[filtered_df["區主管"] == manager]
    if dept_id:
        filtered_df = filtered_df[filtered_df["部門編號"] == dept_id]
    if emp_id:
        filtered_df = filtered_df[filtered_df["員編"] == emp_id]
    if name:
        filtered_df = filtered_df[filtered_df["人員姓名"] == name]

    st.subheader("📋 查詢結果：門店 考核總表")
    st.dataframe(filtered_df.style.format(precision=1))

    st.subheader("📈 等級分布表")
    st.dataframe(df_dist)
