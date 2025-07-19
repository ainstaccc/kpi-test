import streamlit as st

def display_summary_table(df):
    st.markdown("### 📋 門店 考核總表")
    if not df.empty:
        st.dataframe(df.iloc[:, :11])
    else:
        st.warning("查無資料")

def display_efficiency_table(df):
    st.markdown("### 📊 人效分析")
    if not df.empty:
        st.dataframe(df.iloc[:, :15])
    else:
        st.warning("查無資料")

def display_detail_tables(df_mgr, df_staff):
    st.markdown("### 🧾 考核明細")
    st.markdown("#### ➤ 店長／副店 考核")
    if not df_mgr.empty:
        st.dataframe(df_mgr.iloc[:, 1:28])
    else:
        st.info("無對應店主管資料")

    st.markdown("#### ➤ 店員／儲備 考核")
    if not df_staff.empty:
        st.dataframe(df_staff.iloc[:, 1:28])
    else:
        st.info("無對應店員資料")

def display_grade_distribution(df):
    st.markdown("### 📈 考核等級分布")
    st.dataframe(df)
