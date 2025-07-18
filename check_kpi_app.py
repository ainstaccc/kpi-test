
import streamlit as st
import pandas as pd
import os
from glob import glob

st.set_page_config(layout="wide")
st.title("門市考核資料自動檢查")

@st.cache_data
def load_latest_kpi_file(folder_path):
    excel_files = sorted(glob(os.path.join(folder_path, "*.xlsx")), reverse=True)
    if not excel_files:
        return None, None
    for file_path in excel_files:
        try:
            df = pd.read_excel(file_path, sheet_name="門店 考核總表", header=1)
            month = pd.read_excel(file_path, sheet_name="門店 考核總表", nrows=1).columns[0]
            return df, month
        except Exception as e:
            continue
    return None, None

folder = "excel_files"
os.makedirs(folder, exist_ok=True)

uploaded_files = st.file_uploader("請上傳考核Excel檔案", type=["xlsx"], accept_multiple_files=True)
if uploaded_files:
    for f in uploaded_files:
        with open(os.path.join(folder, f.name), "wb") as out_file:
            out_file.write(f.read())

df, month = load_latest_kpi_file(folder)
if df is not None:
    st.success(f"成功載入最新月份考核資料：{month}")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("無法讀取任何考核Excel檔案，請確認格式是否正確。")
