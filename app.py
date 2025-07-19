
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

def filter_data(df, col, keyword):
    if keyword:
        return df[df[col].astype(str).str.contains(keyword)]
    return df

def main():
    st.title("📊 門市考核查詢系統")
    df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

    st.markdown(f"### 🔎 查詢條件（{summary_month}）")
    st.caption("⚠️ 區主管、部門編號、員工編號、姓名、查詢月份 擇一填寫即可，避免多重條件造成錯誤")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    keyword_mgr = col1.text_input("區主管")
    keyword_dept = col2.text_input("部門編號")
    keyword_id = col3.text_input("員工編號")
    keyword_name = col4.text_input("姓名")
    keyword_month = st.text_input("查詢月份", value=summary_month)

    filtered_summary = df_summary.copy()
    if keyword_month and keyword_month != summary_month:
        st.warning(f"⚠️ 資料月份為 {summary_month}，查詢月份「{keyword_month}」無效，將使用資料月份查詢。")

    if keyword_mgr:
        filtered_summary = filter_data(filtered_summary, "區主管", keyword_mgr)
    if keyword_dept:
        filtered_summary = filter_data(filtered_summary, "部門編號", keyword_dept)
    if keyword_id:
        filtered_summary = filter_data(filtered_summary, "員工編號", keyword_id)
    if keyword_name:
        filtered_summary = filter_data(filtered_summary, "人員姓名", keyword_name)

    st.markdown("## 📋 查詢結果：門店 考核總表")
    st.dataframe(filtered_summary, use_container_width=True)

    st.markdown("## 📈 等級分布表")
    st.dataframe(df_dist, use_container_width=True)

    st.markdown("## 👥 查詢結果：人效分析")
    st.dataframe(filter_data(df_eff, "員工編號", keyword_id), use_container_width=True)

    st.markdown("## 🧑‍💼 查詢結果：店長/副店 考核明細")
    st.dataframe(filter_data(df_mgr, "員工編號", keyword_id), use_container_width=True)

    st.markdown("## 👕 查詢結果：店員/儲備 考核明細")
    st.dataframe(filter_data(df_staff, "員工編號", keyword_id), use_container_width=True)

if __name__ == "__main__":
    main()
