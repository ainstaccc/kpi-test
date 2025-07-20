現在開始建立「米斯特 門市月考核查詢平台（Python Streamlit 版）」

依以下提供的資訊進行開發：

1. 資料來源
⬆️ 上傳含考核資料的 Excel 檔案(如附件:2025.06_MST-PA.xlsx)>檔案已存在GitHub
https://github.com/ainstaccc/kpi-checker/tree/main
查詢結果-標題列顏色需與EXCEL表檔案一致

2. 查詢方式
請勾選預計查詢欄位與方式：
#區域（下拉選單）比對檔案來源:[分頁]門店 考核總表  B欄(區主管)>輸出區主管相符的完整資料列
選項:
李政勳
鄧思思
林宥儒
羅婉心
王建樹
楊茜聿
陳宥蓉
吳岱侑
翁聖閔
黃啟周
栗晉屏
王瑞辰

#部門編號（選填）比對檔案來源:[分頁]門店 考核總表 C欄(部門編號)>輸出部門編號相符的完整資料列
#員工編號（選填）比對檔案來源:[分頁]門店 考核總表 E欄(員編)>輸出員工編號相符的完整資料列
#人員姓名（選填）比對檔案來源:[分頁]門店 考核總表 F欄(人員姓名)>輸出人員姓名相符的完整資料列
#查詢月份（下拉選單）比對檔案來源:[分頁]門店 考核總表 A1(2025/06)>預設2025/06，目前只有一個選項
(查詢按鈕)

查詢按鈕下方顯示：本次考核等級分布
來源:[分頁]等級分布 A1:N15

----------
3. 查詢結果：分上中下三部份 
依查詢條件比對各分頁中對應欄位，抓取符合項目的所有筆數，寫入指定的欄位資訊，
查詢結果 人效分析：(如圖)如為員編則視為文字(不須千分位樣式)、如為數字格式則寫入至小數點後一位、如為相對績效或會員率資訊則顯示為%百分比格式 

<上>門店 考核總表
[來源分頁]門店 考核總表(固定標題列A2:K2)
考核分類	
區主管	
部門編號	
部門名稱	
員編	
人員姓名	
考核項目分數	
管理項目分數	
等級	
需訪談	
重點關注
*對應查詢條件B:F欄=區主管	部門編號	部門名稱	員編	人員姓名 
輸出對應資料的A:K欄完整資料(固定標題列A2:K2，共11欄) 
----------
<中>人效分析
[來源分頁]人效分析(固定標題列A2:O2)
區主管	
部門編號	
部門名稱	
員編	
人員姓名	
職務名稱	
個績目標	
個績貢獻	
個績達成%	
品牌客單價	
個人客單價	
客單相對績效	
品牌結帳會員率	
個人結帳會員率	
會員相對績效
 *對應查詢條件A:E欄=區主管	部門編號	部門名稱	員編	人員姓名 
寫入對應資料的A:O欄完整資料(固定標題列A2:O2，共15欄) 
*人效分析欄格式：I、L、M、N、O五欄皆寫入為百分比格式
----------
<下>考核明細(先寫店主管區塊、再寫店員區塊，固定標題列)
[來源分頁]店長副店 考核明細(固定標題列B2:AB2)
總分	
級別	
部門編號	
部門名稱	
員編	
人員姓名	
考核分類	
區主管	
考核當月營收	
考核當月目標	
(1)營收達成	
(2)YOY加分項	
業績項目分數	
班表異常	
出勤異常	
管理分數_人資	
罰款	
帳差	
督導表	
管理分數_財務	
驗收	
驗退	
管理分數_商控	
服務客訴	
管理分數_服務	
B+C總計30	
教育訓練加分項 
*對應查詢條件D:I欄=部門編號	部門名稱	員編	人員姓名	考核分類	區主管  
寫入對應資料的B:AB欄完整資料(固定標題列B2:AB2，共27欄) 
**若無對應資料，則顯示標題列即可
----------
[來源分頁]店員儲備 考核明細(固定標題列B2:AB2)
總分	
級別	
部門編號	
店櫃名稱	
員編	
人員姓名	
考核分類	
區主管	
考核當月營收	
考核當月目標	
(1)營收達成	
(2)YOY加分項	
店鋪業績分數	
(3)個績達成	
個績分數	
(4)個人客單	
業績項目總分	
個人出勤	
請假曠職	
管理分數B1	
教育訓練	
會員結帳	
管理分數B2	
個人罰單	
店鋪服務	
管理分數C	
B+C總計30
*對應查詢條件D:I欄=部門編號	部門名稱	員編	人員姓名	考核分類	區主管  
寫入對應資料的B:AB欄完整資料(固定標題列B2:AB2，共27欄) 
**若無對應資料，則顯示標題列即可
----------
最下方以紅字醒目提示： 
※如對分數有疑問，請洽區主管/品牌經理說明。 



4. 權限需求：
限定帳號清單（請提供 Gmail 清單）
區域(對應區主管欄)	gmail帳號
李政勳	fabio89608@gmail.com
鄧思思	124453221s@gmail.com
林宥儒	yolu902@gmail.com
羅婉心	a6108568@gmail.com
王建樹	Wmksue12976@gmail.com
楊茜聿	aqianyu8@gmail.com
陳宥蓉	happy0623091@gmail.com
吳岱侑	cvcv0897@gmail.com
翁聖閔	minkatieweng@gmail.com
黃啟周	a0956505289@gmail.com
栗晉屏	Noncks@gmail.com
王瑞辰	vicecolife0969@gmail.com

部門編號	部門名稱	gmail帳號
LM018	Life8台北西門誠品店(LAKW)	life8x34@gmail.com
LM028	Life8新北宏匯廣場店(LAK)	life8x45@gmail.com
LM040	Life8台北武昌誠品店(LAKWE)	lm040@life8.com.tw
LM007	Life8台北信義A11店(L)	life8x25@gmail.com
LM019	Life8宜蘭新月店(LW)	life8x36@gmail.com
LM021	Life8基隆摩亞時尚店(LAKW)	life8x40@gmail.com
LM030	Life8新北新店裕隆城(LW)	life8x48@gmail.com
LM038	Life8新北板橋誠品(LW)	lm038@life8.com.tw
LM036	Life8新北永和比漾(LW)	life8x60@gmail.com
LM046	Life8台北信義ATT	life8x64@gmail.com
LM033	Life8南港LaLaPort	life8x65@gmail.com
LS002	Life8桃園華泰店(LE)	life8x13@gmail.com
LM016	Life8桃園統領店	life8x31@gmail.com
LM004	Life8新北中和環球店(LW)	life8x19@gmail.com
LM023	Life8台北南港CITYLI(LW)	life8x39@gmail.com
LM026	Life8新北板橋環球店(LAKW)	life8x43@gmail.com
LM024	Life8新北樹林秀泰店	life8x41@gmail.com
LM031	Life8台北美麗華店(LAKWE)	life8x57@gmail.com
LM035	Life8新北汐止iFG遠雄廣場(LW)	life8x58@gmail.com
LM039	Life8新店小碧潭站店(LAKWE)	lm039@life8.com.tw
LM042	Life8桃園台茂(LW)	life8x61@gmail.com
LM047	Life8台北遠企	life8x66@gmail.com
LM022	Life8台中LLP店(LAKWE)	life8x46@gmail.com
LS005	Life8台中麗寶店(LAKWE)	life8x17@gmail.com
LM011	Life8台中文心秀泰店	life8x23@gmail.com
LM014	Life8台中老虎城店(LAK)	life8x29@gmail.com
LM015	Life8台中SOGO店(LAKWE)	life8x30@gmail.com
LM032	Life8台中誠品480店(LAK)	life8x56@gmail.com
LS004	Life8台中三井店(LE)	life8x38@gmail.com
LM002	Life8苗栗尚順店(LAKE)	life8x16@gmail.com
LM003	Life8台中新時代店(LW)	life8x18@gmail.com
LC001	Life8台中勤美旗艦店	lc001@life8.com.tw
LC002	Life8台中松竹旗艦店	life8x63@gmail.com
LK013	Life8新竹巨城	
LM013	Life8嘉義秀泰店(LAKEM)	life8x28@gmail.com
LM006	Life8高雄夢時代店(LKWEM)	life8x20@gmail.com
LM001	Life8高雄SKM店(LAKE)	life8x14@gmail.com
LM009	Life8屏東環球店(LAK)	life8x21@gmail.com
LM020	Life8高雄岡山樂購店	life8x42@gmail.com
LM034	Life8高雄左營新光(LW)	life8x47@gmail.com
LM037	Life8高雄義享天地(LAKW)	lm037@life8.com.tw
LM041	Life8台南南紡店(LW)	
LM048	Life8高雄大遠百	life8x69@gmail.com
LS001	Life8高雄義大A區店(LAKW)	life8x12@gmail.com
LS003	Life8高雄義大C區店(LW)	life8x24@gmail.com
LM005	Life8台南小西門店(LAKW)	life8x03@gmail.com
LM017	Life8台南Focus店(LW)	life8x32@gmail.com
LM045	Life8嘉義耐斯	life8x62@gmail.com
LM044	Life8台南碳佐店(LAKW)	life8x67@gmail.com
AM005	ALL WEARS新北中和環球店(AKW	allwears08@gmail.com
AM007	ALL WEARS桃園台茂店(AK)	allwears10@gmail.com
AM010	ALL WEARS台北京站(AKW)	allwears16@gmail.com
AM015	ALL WEARS新北新店裕隆城(AKW	allwears20@gmail.com
AS001	ALL WEARS台中麗寶店(AKW)	life8x35@gmail.com
AS002	ALL WEARS台中三井店(AKW)	allwears04@gmail.com
AM001	ALL WEARS台中新時代店(AKW)	life8x33@gmail.com
AM004	ALL WEARS台中大遠百店(AKW)	allwears05@gmail.com
AM003	ALL WEARS高雄夢時代店(AKW)	allwears07@gmail.com
AS007	ALL WEARS台南三井店(AKW)	allwears15@gmail.com
WS003	WILDMEET桃園華泰店(WAK)	wildmeet08@gmail.com
WM007	WILDMEET台北京站(WN)	wildmeet09@gmail.com
WM009	WILDMEET新光南西(WN)	wildmeet07@gmail.com
WS007	WILDMEET林口三井店(WAKN)	wildmeet13@gmail.com
WM012	WILDMEET新北宏匯(WN)	wildmeet14@gmail.com
WM011	WILDMEET桃園大江購物(WAKN)	wildmeet15@gmail.com
WS001	WILDMEET台中麗寶店(WAKN)	wildmeet02@gmail.com
WM006	WILDMEET台中老虎城店(WN)	wildmeet10@gmail.com
WS009	WILDMEET-WM苗栗尚順(WN)	wildmeet11@gmail.com
WS002	WILDMEET高雄SKM店(WN)	wildmeet03@gmail.com
WM003	WILDMEET嘉義秀泰店(WN)	wildmeet04@gmail.com
WM005	WILDMEET屏東環球店(WN)	wildmeet06@gmail.com
WM010	WILDMEET新光台南中山(WAK)	wildmeet12@gmail.com		
BS001	BOYLONDON林口三井店(BN)	boylondonx01@gmail.com
BS002	BOYLONDON台中三井店(BN)	boylondonx02@gmail.com
BM001	BOYLONDON台中LaLaport店	boylondonx03@gmail.com
BS003	BOYLONDON台南三井店(BN)	boylondonx04@gmail.com
MM001	Mollifix台北復興SOGO(M)	mollifix01@gmail.com
MM003	Mollifix台北南西新光(ME)	mollifix03@gmail.com
MM008	Mollifix台北京站(ME)	mollifix04@gmail.com
MM007	Mollifix桃園大江(ME)	mollifix06@gmail.com
MM010	Mollifix台北南港City(ME)	mollifix07@gmail.com
MM006	Mollifix台中LLP(ME)	mollifix08@gmail.com
MM009	Mollifix高雄漢神巨蛋(ME)	mollifix09@gmail.com
MM004	Mollifix台南小西門(ME)	mollifix10@gmail.com
NM001	NonSpace南港LLP(NZ)	nonspace02@gmail.com
NM003	NonSpace中和環球(NZ)	nonspace03@gmail.com


-----2041-----
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
    st.image("https://github.com/ainstaccc/kpi-checker/raw/main/2025.06%20%E8%80%83%E6%A0%B8%E7%AD%89%E7%B4%9A%E5%88%86%E5%B8%83.jpg", caption="2025/06 📈本月考核等級分布", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔎 查詢", type="primary"):

        # Filter logic for summary
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
        if emp_id:
            eff_mask &= df_eff["員編"].astype(str) == emp_id
            mgr_mask &= df_mgr["員編"].astype(str) == emp_id
            staff_mask &= df_staff["員編"].astype(str) == emp_id
        if emp_name:
            eff_mask &= df_eff["人員姓名"].str.contains(emp_name)
            mgr_mask &= df_mgr["人員姓名"].str.contains(emp_name)
            staff_mask &= df_staff["人員姓名"].str.contains(emp_name)

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
        st.dataframe(df_eff_result_fmt.style.format(format_dict), use_container_width=True)




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
