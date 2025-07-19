import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

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

def format_eff(df):
    if df.empty:
        return df
    df = df.copy()
    for col in ["個績目標", "個績貢獻", "品牌 客單價", "個人 客單價"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').round(1)
    for col in ["個績達成%", "客單 相對績效", "品牌 結帳會員率", "個人 結帳會員率", "會員 相對績效"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x}%" if pd.notnull(x) else x)
    return df

def main():
    st.markdown("<h3>📊 米斯特 門市 工作績效月考核查詢系統</h3>", unsafe_allow_html=True)

    df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month = load_data()

    with st.expander("🔍 查詢條件", expanded=True):
        st.markdown("**🔺查詢條件任一欄即可，避免多重條件造成查詢錯誤。**")
        col1, col2 = st.columns(2)
        area = col1.selectbox("區域/區主管", options=[
            "", "李政勳", "鄧思思", "林宥儒", "羅婉心", "王建樹", "楊茜聿", 
            "陳宥蓉", "吳岱侑", "翁聖閔", "黃啟周", "栗晉屏", "王瑞辰"
        ])
        dept_code = col2.text_input("部門編號/門店編號")
        emp_id = st.text_input("員工編號")
        emp_name = st.text_input("人員姓名")
        month = st.selectbox("查詢月份", options=["2025/06"])

    st.markdown(" <br><br>", unsafe_allow_html=True)
    st.image("https://github.com/ainstaccc/kpi-checker/raw/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg", caption="2025/06 本月考核等級分布", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔎 查詢", type="primary"):
        st.subheader("📈 本月考核等級分布")
        st.dataframe(df_dist, use_container_width=True)

        # Filter logic
        mask = pd.Series(True, index=df_summary.index)
        if area:
            mask &= df_summary["區主管"] == area
        if dept_code:
            mask &= df_summary["部門編號"] == dept_code
        if emp_id:
            mask &= df_summary["員編"].astype(str) == emp_id
        if emp_name:
            mask &= df_summary["人員姓名"].str.contains(emp_name)

        df_result = df_summary[mask]
        df_eff_result = df_eff[mask]
        df_mgr_result = df_mgr[mask]
        df_staff_result = df_staff[mask]

        st.markdown("## 🧾 門店考核總表")
        st.dataframe(df_result, use_container_width=True)

        st.markdown("## 👥 人效分析")
        df_eff_result_fmt = format_eff(df_eff_result)
        st.dataframe(df_eff_result_fmt, use_container_width=True)

        st.markdown("## 👔 店長/副店 考核明細")
        st.dataframe(df_mgr_result if not df_mgr_result.empty else df_mgr.head(0), use_container_width=True)

        st.markdown("## 👟 店員/儲備 考核明細")
        st.dataframe(df_staff_result if not df_staff_result.empty else df_staff.head(0), use_container_width=True)

        # 匯出結果按鈕
        export_zip = BytesIO()
        with zipfile.ZipFile(export_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("門店考核總表.csv", df_result.to_csv(index=False, encoding="utf-8-sig"))
            zf.writestr("人效分析.csv", df_eff_result.to_csv(index=False, encoding="utf-8-sig"))
            zf.writestr("店長副店 考核明細.csv", df_mgr_result.to_csv(index=False, encoding="utf-8-sig"))
            zf.writestr("店員儲備 考核明細.csv", df_staff_result.to_csv(index=False, encoding="utf-8-sig"))

        st.download_button(
            label="📥 匯出查詢結果（Excel ZIP）",
            data=export_zip.getvalue(),
            file_name="查詢結果.zip",
            mime="application/zip"
        )

        st.markdown("<p style='color:red;font-weight:bold;font-size:16px;'>※如對分數有疑問，請洽區主管/品牌經理說明。</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
