import streamlit as st
import pandas as pd
from io import BytesIO

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"

@st.cache_data(ttl=3600)
def load_data():
    try:
        xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
        sheet_names = xls.sheet_names
        required_sheets = ["門店 考核總表", "人效分析", "店長副店 考核明細", "店員儲備 考核明細", "等級分布"]
        for name in required_sheets:
            if name not in sheet_names:
                raise ValueError(f"❌ 缺少必要工作表：{name}")

        df_summary = xls.parse("門店 考核總表", header=1)
        df_eff = xls.parse("人效分析", header=1)
        df_mgr = xls.parse("店長副店 考核明細", header=1)
        df_staff = xls.parse("店員儲備 考核明細", header=1)
        df_dist = xls.parse("等級分布", header=None, nrows=15, usecols="A:N")

        try:
            summary_month = xls.parse("門店 考核總表", header=None, nrows=1).iloc[0, 0]
        except Exception:
            summary_month = "未知月份"

        return df_summary, df_eff, df_mgr, df_staff, df_dist, summary_month
    except Exception as e:
        st.error(f"❌ 資料載入失敗：{e}")
        return None, None, None, None, None, None


def format_eff(df):
    if df is None or df.empty:
        return pd.DataFrame()
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
    if df_summary is None:
        st.stop()  # 終止執行

    with st.expander("🔍 查詢條件", expanded=True):
        st.markdown("**🔺查詢條件任一欄即可，避免多重條件造成查詢錯誤。**")
        col1, col2 = st.columns(2)
        area = col1.selectbox("區域/區主管", options=[
            "", "李政勳", "林宥儒", "羅婉心", "王建樹", "楊茜聿",
            "陳宥蓉", "吳岱侑", "翁聖閔", "黃啓周", "栗晉屏", "王瑞辰"
        ])
        dept_code = col2.text_input("部門編號/門店編號")
        month = st.selectbox("查詢月份", options=["2025/06"])

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("🔎 查詢", type="primary"):
        try:
            # ✅ 篩選處理
            df_result = df_summary.copy()
            if area:
                df_result = df_result[df_result["區主管"] == area]
            if dept_code:
                df_result = df_result[df_result["部門編號"] == dept_code]

            df_eff_result = df_eff.copy()
            if area:
                df_eff_result = df_eff_result[df_eff_result["區主管"] == area]
            if dept_code:
                df_eff_result = df_eff_result[df_eff_result["部門編號"] == dept_code]

            df_mgr_result = df_mgr.copy()
            if area:
                df_mgr_result = df_mgr_result[df_mgr_result["區主管"] == area]
            if dept_code:
                df_mgr_result = df_mgr_result[df_mgr_result["部門編號"] == dept_code]

            df_staff_result = df_staff.copy()
            if area:
                df_staff_result = df_staff_result[df_staff_result["區主管"] == area]
            if dept_code:
                df_staff_result = df_staff_result[df_staff_result["部門編號"] == dept_code]

            # ✅ 顯示查詢結果
            st.image("https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_grade.jpg", use_column_width=True)

            st.markdown("## 🧾 門店考核總表")
            st.markdown(f"共查得：{len(df_result)} 筆")
            st.dataframe(df_result.iloc[:, 2:11], use_container_width=True)

            st.markdown("## 👥 人效分析")
            df_eff_fmt = format_eff(df_eff_result)
            st.markdown(f"共查得：{len(df_eff_fmt)} 筆")
            st.dataframe(df_eff_fmt, use_container_width=True)

            st.markdown("## 👔 店長/副店 考核明細")
            df_mgr_display = pd.concat([
                df_mgr_result.iloc[:, 1:7],
                df_mgr_result.iloc[:, 11:28]
            ], axis=1)
            st.markdown(f"共查得：{len(df_mgr_display)} 筆")
            st.dataframe(df_mgr_display, use_container_width=True)

            st.markdown("## 👟 店員/儲備 考核明細")
            df_staff_display = pd.concat([
                df_staff_result.iloc[:, 1:7],
                df_staff_result.iloc[:, 11:28]
            ], axis=1)
            st.markdown(f"共查得：{len(df_staff_display)} 筆")
            st.dataframe(df_staff_display, use_container_width=True)

            st.markdown("<p style='color:red;font-weight:bold;font-size:16px;'>※如對分數有疑問，請洽區主管/品牌經理說明。</p>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ 查詢過程發生錯誤：{e}")


if __name__ == "__main__":
    main()
