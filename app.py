import streamlit as st
import pandas as pd

# 將此處改為你 repo 的 raw 檔案連結
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

df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

st.set_page_config(page_title="📋 米斯特 門市月考核查詢平台", layout="wide")
st.title("📋 米斯特 門市月考核查詢平台")

st.markdown(f"#### 📅 本次查詢月份：{summary_month}")

# 查詢條件（皆為非必填）
col1, col2 = st.columns(2)
with col1:
    area = st.selectbox("區主管", options=[""] + sorted(df_summary["區主管"].dropna().unique().tolist()))
    dept = st.selectbox("部門編號", options=[""] + sorted(df_summary["部門編號"].dropna().astype(str).unique().tolist()))
with col2:
    emp_id = st.text_input("員工編號")
    name = st.text_input("姓名")

st.markdown("#### 📊 本次考核等級分布")
st.dataframe(df_dist, use_container_width=True)

if st.button("查詢"):
    df_f = df_summary.copy()
    if area: df_f = df_f[df_f["區主管"] == area]
    if dept: df_f = df_f[df_f["部門編號"].astype(str) == dept]
    if emp_id: df_f = df_f[df_f["員編"].astype(str).str.contains(emp_id)]
    if name: df_f = df_f[df_f["員工姓名"].astype(str).str.contains(name)]

    st.markdown("### ✅ 門店 考核總表")
    cols1 = ['考核分類','區主管','部門編號','部門名稱','員編','人員姓名','考核項目分數','管理項目分數','等級','需訪談','重點關注']
    st.dataframe(df_f[cols1] if not df_f.empty else pd.DataFrame(columns=cols1), use_container_width=True)

    st.markdown("### 📊 人效分析")
    emp_ids = df_f["員編"].unique()
    df_e = df_eff[df_eff["員編"].isin(emp_ids)]
    st.dataframe(df_e if not df_e.empty else pd.DataFrame(columns=df_eff.columns), use_container_width=True)

    st.markdown("### 📝 店長／副店 考核明細")
    df_m = df_mgr[df_mgr["員編"].isin(emp_ids)]
    st.dataframe(df_m if not df_m.empty else pd.DataFrame(columns=df_mgr.columns), use_container_width=True)

    st.markdown("### 🧾 店員／儲備 考核明細")
    df_s = df_staff[df_staff["員編"].isin(emp_ids)]
    st.dataframe(df_s if not df_s.empty else pd.DataFrame(columns=df_staff.columns), use_container_width=True)

    st.markdown("#### ※如對分數有疑問，請洽區主管／品牌經理說明。")
