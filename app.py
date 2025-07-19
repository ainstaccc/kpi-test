import streamlit as st
import pandas as pd
from utils.auth import check_login
from utils.loaders import load_excel_data, filter_data
from utils.display import display_summary_table, display_efficiency_table, display_detail_tables, display_grade_distribution

st.set_page_config(page_title="米斯特門市月考核查詢平台", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.session_state.authenticated = check_login()

if st.session_state.authenticated:
    st.title("米斯特門市月考核查詢平台")

    df_summary, df_eff, df_mgr, df_staff, df_grade, summary_month = load_excel_data()

    with st.sidebar:
        st.header("查詢條件")
        selected_manager = st.selectbox("區域 / 區主管", [
            "李政勳", "鄧思思", "林宥儒", "羅婉心", "王建樹", "楊茜聿",
            "陳宥蓉", "吳岱侑", "翁聖閔", "黃啟周", "栗晉屏", "王瑞辰"
        ])
        dept_id = st.text_input("部門編號 (選填)")
        emp_id = st.text_input("員工編號 (選填)")
        emp_name = st.text_input("人員姓名 (選填)")
        st.selectbox("查詢月份", [summary_month], index=0)
        query = st.button("查詢")

    if query:
        st.subheader("查詢結果")
        df_filtered = filter_data(df_summary, df_eff, df_mgr, df_staff,
                                  selected_manager, dept_id, emp_id, emp_name)
        display_summary_table(df_filtered["summary"])
        display_efficiency_table(df_filtered["eff"])
        display_detail_tables(df_filtered["mgr"], df_filtered["staff"])
        display_grade_distribution(df_grade)

        st.markdown("※如對分數有疑問，請洽區主管/品牌經理說明。")
