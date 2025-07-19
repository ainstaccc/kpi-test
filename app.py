import streamlit as st
import pandas as pd
from io import BytesIO
import requests

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"
IMG_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg"

@st.cache_data(ttl=3600)
def load_data():
    xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
    df_summary = xls.parse("門店 考核總表", header=1, usecols="A:K")
    df_eff = xls.parse("人效分析", header=1)
    df_mgr = xls.parse("店長副店 考核明細", header=1, usecols="B:AB")
    df_staff = xls.parse("店員儲備 考核明細", header=1, usecols="B:AB")
    summary_month = xls.parse("門店 考核總表", nrows=1).columns[0]
    return df_summary, df_eff, df_mgr, df_staff, summary_month

def format_efficiency(df):
    percent_cols = ['I', 'L', 'M', 'N', 'O']
    col_names = df.columns
    for col in percent_cols:
        if col in col_names:
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100
    return df

def generate_excel(summary, eff, mgr, staff):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        summary.to_excel(writer, sheet_name="門店 考核總表", index=False)
        eff.to_excel(writer, sheet_name="人效分析", index=False)
        mgr.to_excel(writer, sheet_name="店長副店 考核明細", index=False)
        staff.to_excel(writer, sheet_name="店員儲備 考核明細", index=False)
    output.seek(0)
    return output

# 載入資料
df_summary, df_eff, df_mgr, df_staff, summary_month = load_data()
df_eff = format_efficiency(df_eff)

st.set_page_config(page_title="米斯特門市考核查詢平台", layout="wide")
st.title("米斯特門市考核查詢平台")
st.markdown(f"## 查詢月份：{summary_month}")
st.markdown("### 查詢條件")
st.markdown("<span style='color:red'>查詢條件擇一填寫即可，避免多重條件造成錯誤。</span>", unsafe_allow_html=True)

# 查詢欄位
col1, col2 = st.columns(2)
with col1:
    q_mgr = st.text_input("區主管")
    q_dept = st.text_input("部門編號")
with col2:
    q_id = st.text_input("員工編號")
    q_name = st.text_input("姓名")

# 查詢按鈕 + 顯示圖片
if not any([q_mgr, q_dept, q_id, q_name]):
    st.image(IMG_URL, caption="本次考核等級分布")

if st.button("查詢"):
    def filter_df(df):
        filtered = df.copy()
        if q_mgr: filtered = filtered[filtered["區主管"] == q_mgr]
        if q_dept: filtered = filtered[filtered["部門編號"] == q_dept]
        if q_id: filtered = filtered[filtered["員編"] == q_id]
        if q_name: filtered = filtered[filtered["人員姓名"].astype(str).str.contains(q_name)]
        return filtered

    # 各表格查詢結果
    result1 = filter_df(df_summary)
    result2 = filter_df(df_eff)
    result3 = filter_df(df_mgr)
    result4 = filter_df(df_staff)

    # 顯示查詢結果
    st.subheader("1️⃣ 門店考核總表")
    st.dataframe(result1.round(1), use_container_width=True)

    st.subheader("2️⃣ 人效分析")
    st.dataframe(result2.style.format({col: '{:.1%}' for col in ['I', 'L', 'M', 'N', 'O']}), use_container_width=True)

    st.subheader("3️⃣ 店長副店 考核明細")
    st.dataframe(result3.round(1), use_container_width=True)

    st.subheader("4️⃣ 店員儲備 考核明細")
    st.dataframe(result4.round(1), use_container_width=True)

    # 匯出按鈕
    st.markdown("### 📥 匯出結果")
    excel_data = generate_excel(result1, result2, result3, result4)
    st.download_button(
        label="匯出為 Excel（含四分頁）",
        data=excel_data,
        file_name="考核查詢結果.xls",
        mime="application/vnd.ms-excel"
    )
