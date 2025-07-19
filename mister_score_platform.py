
import streamlit as st
import pandas as pd

# Google Sheet 連結設定
sheet_id = "1ncJPKt9RabUuyUOHQrwOWkldctv-TUPQdgcXu3pvz4"
base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="

# 各分頁資料
sheet_urls = {
    "等級分布": base_url + "等級分布",
    "門店 考核總表": base_url + "門店 考核總表",
    "人效分析": base_url + "人效分析",
    "店長副店 考核明細": base_url + "店長/副店 考核明細",
    "店員儲備 考核明細": base_url + "店員/儲備"
}

@st.cache_data(ttl=3600)
def load_data():
    return {name: pd.read_csv(url) for name, url in sheet_urls.items()}

data = load_data()
df_total = data["門店 考核總表"]
df_perf = data["人效分析"]
df_detail_mgr = data["店長副店 考核明細"]
df_detail_staff = data["店員儲備 考核明細"]
df_level = data["等級分布"]

# 介面設定
st.set_page_config(layout="wide")
st.title("📋 米斯特 門市月考核查詢平台")

# 顯示查詢月份
month = str(df_total.columns[0]) if df_total.shape[1] > 0 else "查無月份"
st.subheader(f"📆 查詢月份：{month}")

# 顯示等級分布表格
st.markdown("### 🔢 考核等級分布")
st.dataframe(df_level.head(15), use_container_width=True)

# 取得搜尋條件下拉選單選項
區主管清單 = df_total["區主管"].dropna().unique().tolist()
部門編號清單 = df_total["部門編號"].dropna().unique().tolist()
員工編號清單 = df_total["員編"].dropna().unique().tolist()
姓名清單 = df_total["人員姓名"].dropna().unique().tolist()

# 搜尋欄
with st.expander("🔍 查詢條件", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    selected_manager = col1.selectbox("區主管", options=[""] + 區主管清單)
    selected_dept = col2.selectbox("部門編號", options=[""] + 部門編號清單)
    selected_id = col3.selectbox("員工編號", options=[""] + 員工編號清單)
    selected_name = col4.selectbox("姓名", options=[""] + 姓名清單)

# 條件篩選
mask = pd.Series([True] * len(df_total))
if selected_manager:
    mask &= df_total["區主管"] == selected_manager
if selected_dept:
    mask &= df_total["部門編號"] == selected_dept
if selected_id:
    mask &= df_total["員編"] == selected_id
if selected_name:
    mask &= df_total["人員姓名"] == selected_name

filtered_total = df_total[mask]

# 顯示查詢結果
if not filtered_total.empty:
    st.markdown("### ✅ 門店考核總表")
    show_cols_total = df_total.columns[:11]  # A:K欄
    st.dataframe(filtered_total[show_cols_total], use_container_width=True)

    st.markdown("### 📊 人效分析")
    filtered_perf = df_perf.merge(filtered_total[["區主管", "部門編號", "部門名稱", "員編", "人員姓名"]],
                                  on=["區主管", "部門編號", "部門名稱", "員編", "人員姓名"], how="inner")
    st.dataframe(filtered_perf.iloc[:, :15], use_container_width=True)

    st.markdown("### 🧾 店長／副店 考核明細")
    filtered_detail_mgr = df_detail_mgr.merge(
        filtered_total[["部門編號", "部門名稱", "員編", "人員姓名", "考核分類", "區主管"]],
        on=["部門編號", "部門名稱", "員編", "人員姓名", "考核分類", "區主管"], how="inner"
    )
    if not filtered_detail_mgr.empty:
        st.dataframe(filtered_detail_mgr.iloc[:, 1:28], use_container_width=True)
    else:
        st.dataframe(df_detail_mgr.iloc[1:2, 1:28], use_container_width=True)

    st.markdown("### 🧾 店員／儲備 考核明細")
    filtered_detail_staff = df_detail_staff.merge(
        filtered_total[["部門編號", "部門名稱", "員編", "人員姓名", "考核分類", "區主管"]],
        left_on=["部門編號", "店櫃名稱", "員編", "人員姓名", "考核分類", "區主管"],
        right_on=["部門編號", "部門名稱", "員編", "人員姓名", "考核分類", "區主管"],
        how="inner"
    )
    if not filtered_detail_staff.empty:
        st.dataframe(filtered_detail_staff.iloc[:, 1:28], use_container_width=True)
    else:
        st.dataframe(df_detail_staff.iloc[1:2, 1:28], use_container_width=True)

    st.markdown("#### ※如對分數有疑問，請洽區主管/品牌經理說明。")

else:
    st.warning("請選擇查詢條件後進行查詢。")
