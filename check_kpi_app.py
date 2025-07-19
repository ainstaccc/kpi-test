
import streamlit as st
import pandas as pd

# 頁面設定
st.set_page_config(page_title="📋 米斯特 門市月考核查詢平台", layout="wide")

@st.cache_data
def load_data():
    xlsx = pd.ExcelFile("2025.06_MST-PA.xlsx")
    df_summary = pd.read_excel(xlsx, sheet_name="門店 考核總表", skiprows=1)
    df_summary.columns = ['考核分類', '區主管', '部門編號', '部門名稱', '員編', '人員姓名', '考核項目分數', '管理項目分數', '等級', '需訪談', '重點關注']

    df_perf = pd.read_excel(xlsx, sheet_name="人效分析", skiprows=1)
    df_perf.columns = ['區主管', '部門編號', '部門名稱', '員編', '人員姓名', '職務名稱', '個績目標', '個績貢獻', '個績達成%', '品牌客單價', '個人客單價', '客單相對績效', '品牌結帳會員率', '個人結帳會員率', '會員相對績效']

    df_mgr = pd.read_excel(xlsx, sheet_name="店長/副店 考核明細", skiprows=1)
    df_mgr.columns = pd.read_excel(xlsx, sheet_name="店長/副店 考核明細", nrows=1).columns.tolist()

    df_staff = pd.read_excel(xlsx, sheet_name="店員/儲備 考核明細", skiprows=1)
    df_staff.columns = pd.read_excel(xlsx, sheet_name="店員/儲備 考核明細", nrows=1).columns.tolist()

    df_grade = pd.read_excel(xlsx, sheet_name="等級分布", header=None).iloc[:15, :14]

    return df_summary, df_perf, df_mgr, df_staff, df_grade, pd.read_excel(xlsx, sheet_name="門店 考核總表", nrows=0)

# 載入資料
df_summary, df_perf, df_mgr, df_staff, df_grade, df_summary_raw = load_data()

# 查詢欄位選單
month = pd.read_excel("2025.06_MST-PA.xlsx", sheet_name="門店 考核總表", header=None).iloc[0, 0]
st.title("📋 米斯特 門市月考核查詢平台")
st.markdown(f"#### 🔍 查詢月份：{month}")

# 顯示等級分布
st.markdown("#### 📊 考核等級分布")
st.dataframe(df_grade, use_container_width=True)

# 選項
col1, col2, col3, col4 = st.columns(4)
with col1:
    area = st.selectbox("區主管", sorted(df_summary['區主管'].dropna().unique()))
with col2:
    dept = st.selectbox("部門編號", sorted(df_summary['部門編號'].dropna().unique()))
with col3:
    emp_id = st.selectbox("員工編號", sorted(df_summary['員編'].dropna().unique()))
with col4:
    name = st.selectbox("姓名", sorted(df_summary['人員姓名'].dropna().unique()))

# 查詢
btn = st.button("查詢")
if btn:
    st.subheader("🔎 查詢結果")

    # 第一部份
    st.markdown("#### 📄 門店 考核總表")
    filtered1 = df_summary[
        (df_summary['區主管'] == area) &
        (df_summary['部門編號'] == dept) &
        (df_summary['員編'] == emp_id) &
        (df_summary['人員姓名'] == name)
    ]
    st.dataframe(filtered1, use_container_width=True)

    # 第二部份
    st.markdown("#### 📈 人效分析")
    filtered2 = df_perf[
        (df_perf['區主管'] == area) &
        (df_perf['部門編號'] == dept) &
        (df_perf['員編'] == emp_id) &
        (df_perf['人員姓名'] == name)
    ]
    st.dataframe(filtered2, use_container_width=True)

    # 第三部份
    st.markdown("#### 📝 店長/副店 考核明細")
    filtered3 = df_mgr[
        (df_mgr['部門編號'] == dept) &
        (df_mgr['員編'] == emp_id) &
        (df_mgr['人員姓名'] == name) &
        (df_mgr['區主管'] == area)
    ]
    st.dataframe(filtered3 if not filtered3.empty else df_mgr.iloc[0:0], use_container_width=True)

    st.markdown("#### 🧾 店員/儲備 考核明細")
    filtered4 = df_staff[
        (df_staff['部門編號'] == dept) &
        (df_staff['員編'] == emp_id) &
        (df_staff['人員姓名'] == name) &
        (df_staff['區主管'] == area)
    ]
    st.dataframe(filtered4 if not filtered4.empty else df_staff.iloc[0:0], use_container_width=True)

    st.markdown("###### ※如對分數有疑問，請洽區主管/品牌經理說明。")
