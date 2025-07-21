import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"

@st.cache_data(ttl=3600)
def load_data():
    xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
    df_summary = xls.parse("門店 考核總表", header=1)
    df_eff = xls.parse("人效分析", header=1)  # 不指定 na_values，保留原始錯誤文字
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
        
        # 區域/區主管：可複選
        area_options = df_summary["區主管"].dropna().unique().tolist()
        areas_selected = col1.multiselect("區域/區主管（可複選）", options=area_options)
        
        # 部門選單（格式為 "AM001 - 高雄夢時代"）
        dept_options = df_summary.dropna(subset=["部門編號", "部門名稱"])
        dept_options = dept_options[["部門編號", "部門名稱"]].drop_duplicates()
        dept_options["顯示"] = dept_options["部門編號"] + " - " + dept_options["部門名稱"]
        depts_selected = col2.multiselect("部門編號/門店名稱（可複選）", options=dept_options["顯示"].tolist())


        month = st.selectbox("查詢月份", options=["2025/06"])

    st.markdown(" <br><br>", unsafe_allow_html=True)
    st.image("https://github.com/ainstaccc/kpi-checker/raw/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg", caption="2025/06 📈本月考核等級分布", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔎 查詢", type="primary"):

        # Filter logic for summary
        mask = pd.Series(True, index=df_summary.index)
        if area:
            mask &= df_summary["區主管"] == area
        if dept_code:
            mask &= df_summary["部門編號"] == dept_code


        df_result = df_summary[mask]

        # 分開為其他表格建立遮罩
        eff_mask = pd.Series(True, index=df_eff.index)
        mgr_mask = pd.Series(True, index=df_mgr.index)
        staff_mask = pd.Series(True, index=df_staff.index)

        if area:
            eff_mask &= df_eff["區主管"] == area
            mgr_mask &= df_mgr["區主管"] == area
            staff_mask &= df_staff["區主管"] == area
        if dept_code:
            eff_mask &= df_eff["部門編號"] == dept_code
            mgr_mask &= df_mgr["部門編號"] == dept_code
            staff_mask &= df_staff["部門編號"] == dept_code


        df_eff_result = df_eff[eff_mask]
        df_mgr_result = df_mgr[mgr_mask]
        df_staff_result = df_staff[staff_mask]

        st.markdown("## 🧾 門店考核總表")
        st.markdown(f"共查得：{len(df_result)} 筆")
        st.dataframe(df_result.iloc[:, 2:11], use_container_width=True)

        st.markdown("## 👥 人效分析")
        df_eff_result_fmt = format_eff(df_eff_result)
        
        # 取得所有欄位名稱
        columns = df_eff_result_fmt.columns
        
        # 整數欄（千分位）
        int_columns = [columns[6], columns[7], columns[9], columns[10]]
        # 百分比欄
        percent_columns = columns[11:15]
        
        # 建立格式化字典
        format_dict = {col: "{:,.0f}" for col in int_columns}
        format_dict.update({col: "{:.0%}" for col in percent_columns})
        format_dict[columns[3]] = "{:08.0f}"  # 員編顯示為8位整數
        
        # 顯示
        st.markdown(f"共查得：{len(df_eff_result_fmt)} 筆")
        try:
            st.dataframe(df_eff_result_fmt.style.format(format_dict), use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ 資料格式化失敗，原因：{e}，將改以原始資料顯示")
            st.dataframe(df_eff_result_fmt, use_container_width=True)





        st.markdown("## 👔 店長/副店 考核明細")
        st.markdown(f"共查得：{len(df_mgr_result)} 筆")

        # 只顯示第2～7欄與第12～28欄
        df_mgr_display = pd.concat([
            df_mgr_result.iloc[:, 1:7],    # 第2~7欄
            df_mgr_result.iloc[:, 11:28]   # 第12~28欄
        ], axis=1)

        df_mgr_head_display = pd.concat([
            df_mgr.iloc[:, 1:7], 
            df_mgr.iloc[:, 11:28]
        ], axis=1).head(0)

        st.dataframe(df_mgr_display if not df_mgr_display.empty else df_mgr_head_display, use_container_width=True)

        st.markdown("## 👟 店員/儲備 考核明細")
        st.markdown(f"共查得：{len(df_staff_result)} 筆")

        # 只顯示第2～7欄與第12～28欄
        df_staff_display = pd.concat([
            df_staff_result.iloc[:, 1:7],     # 第2~7欄
            df_staff_result.iloc[:, 11:28]    # 第12~28欄
        ], axis=1)

        df_staff_head_display = pd.concat([
            df_staff.iloc[:, 1:7], 
            df_staff.iloc[:, 11:28]
        ], axis=1).head(0)

        st.dataframe(df_staff_display if not df_staff_display.empty else df_staff_head_display, use_container_width=True)


        st.markdown("<p style='color:red;font-weight:bold;font-size:16px;'>※如對分數有疑問，請洽區主管/品牌經理說明。</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
