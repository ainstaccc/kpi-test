import streamlit as st
import pandas as pd
from helper import load_data, format_efficiency_df, generate_excel

st.set_page_config(layout="wide")

# 讀取資料
df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

st.title(f"📊 {summary_month} 門市考核查詢系統")

# 查詢條件區塊（可擴充）
with st.container():
    with st.expander("🔍 查詢條件", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name_filter = st.text_input("輸入姓名關鍵字查詢", "")
        with col2:
            store_filter = st.text_input("輸入店舖名稱關鍵字查詢", "")

# 匯出按鈕在最上層
col_export = st.columns([0.85, 0.15])
with col_export[1]:
    if st.button("📤 匯出查詢結果 Excel", type="primary"):
        try:
            result1 = df_summary.copy()
            result2 = df_eff.copy()
            result3 = df_mgr.copy()
            result4 = df_staff.copy()
            excel_data = generate_excel(result1, result2, result3, result4)
            st.download_button(label="下載 Excel", data=excel_data, file_name="考核查詢結果.xlsx")
        except Exception as e:
            st.error(f"❌ 匯出失敗：{e}")

# 人效分析區塊
st.subheader("👤 人效分析")
df_eff_formatted = format_efficiency_df(df_eff)
if name_filter:
    df_eff_formatted = df_eff_formatted[df_eff_formatted["人員姓名"].str.contains(name_filter)]
if store_filter:
    df_eff_formatted = df_eff_formatted[df_eff_formatted["部門名稱"].str.contains(store_filter)]
st.dataframe(df_eff_formatted, use_container_width=True)

# 門店考核總表
st.subheader("🏪 門店考核總表")
if name_filter or store_filter:
    df_filtered = df_summary[df_summary["部門名稱"].str.contains(store_filter) & df_summary["店長姓名"].str.contains(name_filter)]
else:
    df_filtered = df_summary
st.dataframe(df_filtered, use_container_width=True)

# 店長副店明細
st.subheader("👨‍💼 店長/副店考核明細")
if name_filter:
    df_mgr = df_mgr[df_mgr["人員姓名"].str.contains(name_filter)]
if store_filter:
    df_mgr = df_mgr[df_mgr["部門名稱"].str.contains(store_filter)]
st.dataframe(df_mgr, use_container_width=True)

# 店員儲備明細
st.subheader("🧍‍♀️ 店員/儲備考核明細")
if name_filter:
    df_staff = df_staff[df_staff["人員姓名"].str.contains(name_filter)]
if store_filter:
    df_staff = df_staff[df_staff["部門名稱"].str.contains(store_filter)]
st.dataframe(df_staff, use_container_width=True)

# 等級分布圖
st.subheader("📈 考核等級分布")
st.image("https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/dist.png")
