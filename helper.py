import pandas as pd
from io import BytesIO

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

def format_efficiency_df(df):
    df = df.copy()
    text_cols = df.columns[:6]
    int_cols = df.columns[[6, 7, 9, 10]]
    pct_cols = df.columns[[8, 11, 12, 13, 14]]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    for col in pct_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int).astype(str) + "%"
    return df

def generate_excel(df1, df2, df3, df4):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, index=False, sheet_name="門店總表")
        df2.to_excel(writer, index=False, sheet_name="人效分析")
        df3.to_excel(writer, index=False, sheet_name="店長副店明細")
        df4.to_excel(writer, index=False, sheet_name="店員儲備明細")
    output.seek(0)
    return output
