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

# 讀取資料
df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

# 設定頁面
st.set_page_config(layout="wide", page_title="米斯特 2025/06 門市月考核查詢")

# 查詢區塊
with st.expander("🔍 請輸入查詢條件"):
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("輸入門店名稱（模糊比對）")
    with col2:
        emp_id = st.text_input("輸入員工工號（完整8碼）")
    with col3:
        emp_name = st.text_input("輸入員工姓名（模糊比對）")

    # 查詢按鈕
    do_query = st.button("🔎 查詢", type="primary")

# 顯示分布圖
st.image(
    "https://github.com/ainstaccc/kpi-checker/raw/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg",
    caption="2025/06 本月考核等級分布",
    use_column_width=True
)

# 查詢邏輯執行
if do_query:
    # 建立各 DataFrame 遮罩
    mask_summary = (
        df_summary["門店名稱"].astype(str).str.contains(store_name) if store_name else True
    ) & (
        df_summary["員工工號"].astype(str) == emp_id if emp_id else True
    ) & (
        df_summary["姓名"].astype(str).str.contains(emp_name) if emp_name else True
    )

    mask_eff = (
        df_eff["門店名稱"].astype(str).str.contains(store_name) if store_name else True
    ) & (
        df_eff["員工工號"].astype(str) == emp_id if emp_id else True
    ) & (
        df_eff["姓名"].astype(str).str.contains(emp_name) if emp_name else True
    )

    mask_mgr = (
        df_mgr["門店名稱"].astype(str).str.contains(store_name) if store_name else True
    ) & (
        df_mgr["員工編號"].astype(str) == emp_id if emp_id else True
    ) & (
        df_mgr["姓名"].astype(str).str.contains(emp_name) if emp_name else True
    )

    mask_staff = (
        df_staff["門店名稱"].astype(str).str.contains(store_name) if store_name else True
    ) & (
        df_staff["員工編號"].astype(str) == emp_id if emp_id else True
    ) & (
        df_staff["姓名"].astype(str).str.contains(emp_name) if emp_name else True
    )

    st.markdown(f"### 📊 查詢結果 - {summary_month}")

    st.subheader("1️⃣ 門店總表")
    st.dataframe(df_summary[mask_summary].head(20), use_container_width=True)

    st.subheader("2️⃣ 人效分析")
    st.dataframe(df_eff[mask_eff].head(20), use_container_width=True)

    st.subheader("3️⃣ 店長／副店 考核明細")
    st.dataframe(df_mgr[mask_mgr].head(20), use_container_width=True)

    st.subheader("4️⃣ 店員／儲備 考核明細")
    st.dataframe(df_staff[mask_staff].head(20), use_container_width=True)

    st.info("🔎 若無資料，請確認是否輸入錯誤。")

# 頁尾
st.caption("📌 本平台由 GPT 協助建置，資料來源：2025/06 考核資料表")
