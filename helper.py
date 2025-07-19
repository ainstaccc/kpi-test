import pandas as pd
from io import BytesIO

FILE_URL = "https://raw.githubusercontent.com/ainstaccc/kpi-checker/main/2025.06_MST-PA.xlsx"

def load_data():
    xls = pd.ExcelFile(FILE_URL, engine="openpyxl")
    df_summary = xls.parse("門店 考核總表", header=1, usecols="A:K")
    df_eff = xls.parse("人效分析", header=1)
    for col in ["I", "L", "M", "N", "O"]:
        if col in df_eff.columns:
            df_eff[col] = pd.to_numeric(df_eff[col], errors='coerce') / 100
            df_eff[col] = df_eff[col].map(lambda x: "{:.2%}".format(x) if pd.notnull(x) else "")
    df_mgr = xls.parse("店長副店 考核明細", header=1, usecols="B:AB")
    df_staff = xls.parse("店員儲備 考核明細", header=1, usecols="B:AB")
    return df_summary, df_eff, df_mgr, df_staff

def filter_data(df, keyword):
    df_str = df.astype(str)
    return df[df_str.apply(lambda row: row.str.contains(keyword, na=False)).any(axis=1)]

def convert_df_to_excel(dfs: dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    output.seek(0)
    return output
