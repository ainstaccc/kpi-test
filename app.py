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

df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

st.set_page_config(page_title="米斯特門市月考核查詢平台", layout="wide")
st.markdown("<style>.big-font { font-size:28px !important; }</style>", unsafe_allow_html=True)

st.image("https://github.com/ainstaccc/kpi-checker/raw/main/banner.png", use_column_width=True)

st.markdown(f"<div class='big-font'>📊 {summary_month} 本月考核等級分布</div>", unsafe_allow_html=True)
st.dataframe(df_dist, use_container_width=True)

st.markdown("## 🔍 本月考核等級分布")
with st.form("query-form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("姓名")
    with col2:
        emp_id = st.text_input("工號")
    with col3:
        store = st.text_input("門店")

    if st.form_submit_button("🔎 查詢", type="primary"):
        result_df = df_mgr[df_mgr["姓名"].astype(str).str.contains(name, na=False)] \
                    if name else df_mgr
        result_df = result_df[result_df["工號"].astype(str).str.contains(emp_id, na=False)] \
                    if emp_id else result_df
        result_df = result_df[result_df["門店"].astype(str).str.contains(store, na=False)] \
                    if store else result_df

        st.markdown("### 查詢結果")
        if not result_df.empty:
            st.dataframe(result_df.head(20), use_container_width=True)
        else:
            st.warning("查無符合條件的資料，請重新輸入查詢條件。")
