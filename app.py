import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO, StringIO, ZipFile

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"
IMAGE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg"

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
            "陳宥蓉", "吳岱侑", "翁聖閔", "黃啓周", "栗晉屏", "王瑞辰"
        ])
        dept_code = col2.text_input("部門編號/門店編號")
        month = st.selectbox("查詢月份", options=["2025/06"])

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 🖼️ 圖片載入防呆
    try:
        res = requests.get(IMAGE_URL)
        res.raise_for_status()
        img = Image.open(BytesIO(res.content))
        st.image(img, caption="2025/06 📈本月考核等級分布", use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ 圖片載入失敗：{e}")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔎 查詢", type="primary"):
        # 建立篩選條件
        mask = pd.Series(True, index=df_summary.index)
        if area:
            mask &= df_summary["區主管"] == area
        if dept_code:
            mask &= df_summary["部門編號"] == dept_code
        df_result = df_summary[mask]

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

        # 顯示區塊
        st.markdown("## 🧾 門店考核總表")
        st.markdown(f"共查得：{len(df_result)} 筆")
        st.dataframe(df_result.iloc[:, 2:11], use_container_width=True)

        st.markdown("## 👥 人效分析")
        df_eff_result_fmt = format_eff(df_eff_result)
        columns = df_eff_result_fmt.columns
        int_columns = [columns[6], columns[7], columns[9], columns[10]]
        percent_columns = columns[11:15]
        format_dict = {col: "{:,.0f}" for col in int_columns}
        format_dict.update({col: "{:.0%}" for col in percent_columns})
        format_dict[columns[3]] = "{:08.0f}"
        st.markdown(f"共查得：{len(df_eff_result_fmt)} 筆")
        try:
            st.dataframe(df_eff_result_fmt.style.format(format_dict), use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ 資料格式化失敗：{e}，改用原始資料顯示")
            st.dataframe(df_eff_result_fmt, use_container_width=True)

        st.markdown("## 👔 店長/副店 考核明細")
        st.markdown(f"共查得：{len(df_mgr_result)} 筆")
        df_mgr_display = pd.concat([df_mgr_result.iloc[:, 1:7], df_mgr_result.iloc[:, 11:28]], axis=1)
        df_mgr_head_display = pd.concat([df_mgr.iloc[:, 1:7], df_mgr.iloc[:, 11:28]], axis=1).head(0)
        st.dataframe(df_mgr_display if not df_mgr_display.empty else df_mgr_head_display, use_container_width=True)

        st.markdown("## 👟 店員/儲備 考核明細")
        st.markdown(f"共查得：{len(df_staff_result)} 筆")
        df_staff_display = pd.concat([df_staff_result.iloc[:, 1:7], df_staff_result.iloc[:, 11:28]], axis=1)
        df_staff_head_display = pd.concat([df_staff.iloc[:, 1:7], df_staff.iloc[:, 11:28]], axis=1).head(0)
        st.dataframe(df_staff_display if not df_staff_display.empty else df_staff_head_display, use_container_width=True)

        # 匯出 Excel
        output_excel = BytesIO()
        with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
            df_result.iloc[:, 2:11].to_excel(writer, sheet_name="門店考核總表", index=False)
            format_eff(df_eff_result).to_excel(writer, sheet_name="人效分析", index=False)
            df_mgr_display.to_excel(writer, sheet_name="店長副店 考核明細", index=False)
            df_staff_display.to_excel(writer, sheet_name="店員儲備 考核明細", index=False)
        output_excel.seek(0)
        st.download_button("📥 匯出查詢結果（Excel）", data=output_excel, file_name="查詢結果.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        st.markdown("<p style='color:red;font-weight:bold;font-size:16px;'>※如對分數有疑問，請洽區主管/品牌經理說明。</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
