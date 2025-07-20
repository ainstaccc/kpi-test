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
    summary_month = xls.parse("門店 考核總表", nrows=1).columns[0]
    return df_summary, df_eff, df_mgr, df_staff, summary_month

st.set_page_config(page_title="門市月考核查詢平台", layout="wide")
st.title("🏪 米斯特門市月考核查詢平台")
st.caption("版本：2025.07 | 維護者：@沛瑜")

df_summary, df_eff, df_mgr, df_staff, summary_month = load_data()

st.markdown("### 🔍 查詢條件")

col1, col2 = st.columns(2)
with col1:
    name_query = st.text_input("員工姓名")
with col2:
    code_query = st.text_input("員工編號")

if st.button("🔎 查詢", type="primary"):
    if not name_query and not code_query:
        st.warning("請輸入員工姓名或編號")
    else:
        def match_condition(df):
            return (
                df["姓名"].astype(str).str.contains(name_query, na=False) if name_query else True
            ) & (
                df["員工編號"].astype(str).str.contains(code_query, na=False) if code_query else True
            )

        mask_summary = match_condition(df_summary)
        mask_eff = match_condition(df_eff)
        mask_mgr = match_condition(df_mgr)
        mask_staff = match_condition(df_staff)

        st.divider()
        st.subheader(f"📋 基本資料與總表（{summary_month}）")
        st.dataframe(df_summary[mask_summary].head(5), use_container_width=True)

        st.subheader("📈 門店人效分析")
        st.dataframe(df_eff[mask_eff].head(5), use_container_width=True)

        st.subheader("🧑‍💼 店長／副店長 考核明細")
        st.dataframe(df_mgr[mask_mgr].head(5), use_container_width=True)

        st.subheader("👕 店員／儲備 考核明細")
        st.dataframe(df_staff[mask_staff].head(5), use_container_width=True)

        st.divider()
        st.image(
            "https://github.com/ainstaccc/kpi-checker/raw/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg",
            caption="2025/06 本月考核等級分布",
            use_column_width=True
        )
