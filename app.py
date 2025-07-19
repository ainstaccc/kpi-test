import streamlit as st
import pandas as pd
from io import BytesIO
from helper import load_data, filter_data, convert_df_to_excel

st.set_page_config(layout="wide")

# UI Elements
st.title("門市考核查詢系統")
query_name = st.text_input("請輸入姓名或工號關鍵字查詢")
show_results = st.button("查詢")

# Display image below the search button
if query_name:
    st.image("https://github.com/ainstaccc/kpi-checker/raw/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg")

if show_results and query_name:
    df_summary, df_eff, df_mgr, df_staff = load_data()
    results = {
        "門店 考核總表": filter_data(df_summary, query_name),
        "人效分析": filter_data(df_eff, query_name),
        "店長副店 考核明細": filter_data(df_mgr, query_name),
        "店員儲備 考核明細": filter_data(df_staff, query_name)
    }

    for title, df in results.items():
        st.subheader(title)
        st.dataframe(df)

    # Export Excel
    output = convert_df_to_excel(results)
    st.download_button(
        label="📥 下載查詢結果 (Excel)",
        data=output,
        file_name="考核查詢結果.xls",
        mime="application/vnd.ms-excel"
    )
