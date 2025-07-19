import streamlit as st
import pandas as pd
from utils.loaders import load_data, filter_data

# 載入資料
df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

# 頁面設定
st.set_page_config(page_title="米斯特門市月考核查詢平台", layout="wide")
st.title("米斯特門市月考核查詢平台")

st.markdown("### 查詢條件")
st.markdown('<span style="color:red">📌 查詢條件擇一填寫即可，避免多重條件造成錯誤。</span>', unsafe_allow_html=True)

# 查詢條件輸入（皆為非必填）
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("姓名（可模糊搜尋）")
    emp_id = st.text_input("員工編號")
with col2:
    dept_code = st.text_input("部門編號")
    manager = st.text_input("區主管")

# 執行查詢
if st.button("查詢"):
    try:
        df_filtered = filter_data(df_summary, df_eff, df_mgr, df_staff, name, emp_id, dept_code, manager)

        if df_filtered.empty:
            st.warning("查無符合資料，請確認查詢條件是否正確。")
        else:
            st.success("查詢成功，以下為查詢結果：")
            # 數值欄位僅顯示小數點後一位
            for col in df_filtered.select_dtypes(include='number').columns:
                df_filtered[col] = df_filtered[col].round(1)
            st.dataframe(df_filtered, use_container_width=True)

    except KeyError as e:
        st.error(f"欄位錯誤：{e}。請確認試算表中的欄位名稱是否正確對應。")
    except Exception as e:
        st.error(f"發生錯誤：{str(e)}")

# 顯示考核月份
with st.expander("目前資料月份"):
    st.write(f"📅 {summary_month}")

# 顯示考核等級分布
st.markdown("### 本次考核等級分布")
st.dataframe(df_dist, use_container_width=True)
