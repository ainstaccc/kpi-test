import pandas as pd

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"

def load_excel_data():
    xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
    df_summary = xls.parse("門店 考核總表", header=1)
    df_eff = xls.parse("人效分析", header=1)
    df_mgr = xls.parse("店長副店 考核明細", header=1)
    df_staff = xls.parse("店員儲備 考核明細", header=1)
    df_grade = xls.parse("等級分布", header=None, nrows=15, usecols="A:N")
    summary_month = xls.parse("門店 考核總表", nrows=1).columns[0]
    return df_summary, df_eff, df_mgr, df_staff, df_grade, summary_month

def filter_data(df_summary, df_eff, df_mgr, df_staff,
                manager, dept_id, emp_id, emp_name):

    cond = df_summary["區主管"] == manager
    if dept_id:
        cond &= df_summary["部門編號"].astype(str).str.contains(dept_id)
    if emp_id:
        cond &= df_summary["員編"].astype(str).str.contains(emp_id)
    if emp_name:
        cond &= df_summary["人員姓名"].astype(str).str.contains(emp_name)

    summary_result = df_summary[cond]
    keys = ["區主管", "部門編號", "部門名稱", "員編", "人員姓名"]
    base = summary_result[keys].drop_duplicates()

    def sub_filter(df, cols):
        merged = df.merge(base, how="inner", on=cols)
        return merged if not merged.empty else df.iloc[0:0]

    eff_result = sub_filter(df_eff, keys)
    mgr_result = sub_filter(df_mgr, ["部門編號", "部門名稱", "員編", "人員姓名", "考核分類", "區主管"])
    staff_result = sub_filter(df_staff, ["部門編號", "店櫃名稱", "員編", "人員姓名", "考核分類", "區主管"])
    return {
        "summary": summary_result,
        "eff": eff_result,
        "mgr": mgr_result,
        "staff": staff_result
    }
