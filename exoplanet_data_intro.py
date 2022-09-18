import streamlit as st
import pandas as pd


page_title = '太陽系外行星資料簡介'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)

st.header('什麼是太陽系外行星?')
st.info('水星、金星、地球、火星、木星、土星、天王星、海王星都是繞行太陽這個恆星的行星，而位於太陽系之外、不繞行太陽轉的行星，稱為[太陽系外行星](https://zh.wikipedia.org/zh-tw/%E5%A4%AA%E9%99%BD%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F)，也常簡稱為系外行星。')

st.header('可以從哪裡取得太陽系外行星的資料？')
st.subheader('NASA系外行星資料庫')
st.info('[NASA系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)網站提供多個與系外行星相關的資料表，讓人查詢系外行星名稱、所繞行的恆星名稱、發現年份、發現方法、繞行恆星一圈的軌道週期、距離地球多遠、質量大小…等資訊。此[頁面](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html)能查閱各資料表欄位所代表的意義。')
with st.expander('圖片解說'):
	st.image(
		'https://media.heptabase.com/v1/images/e336080b-183d-4940-892f-a27e91a48b9b/d1a626a7-f228-41aa-9a87-767301f596b0/NASAExoplanetArchive.png',
		caption='NASA系外行星資料庫網站首頁。點擊左上角的「Confirmed Planets」可以查看「Planetary Systems」資料表，而「Planetary Systems Composite Data」資料表可從右下角進入。'
	)
	st.image(
		'https://media.heptabase.com/v1/images/e336080b-183d-4940-892f-a27e91a48b9b/8da2f51f-ddae-4b0a-845f-b3d667fc9e3f/ConfirmedPlanetsTable.png',
		caption='「Planetary Systems」資料表，不同研究團隊針對同一個行星所作的研究結果會在這張表分別列出。'
	)
	st.image(
		'https://media.heptabase.com/v1/images/e336080b-183d-4940-892f-a27e91a48b9b/51772e03-2a3e-48bb-9a40-0cc24a00bf21/PlanetarySystemsCompositeDataTable.png',
	caption='「Planetary Systems Composite Data」資料表，能一行綜觀同個行星的所有欄位值。點擊左上方的「Download Table」可將資料表以CSV格式匯出。'
	)

with st.expander('上傳從NASA系外行星資料庫所匯出的CSV檔，以呈現資料表'):
	uploaded_csv = st.file_uploader('選擇要上傳的CSV檔')
	if uploaded_csv is not None:
		exoplanet_table = pd.read_csv(uploaded_csv)
		st.text('系外行星資料表')
		st.dataframe(exoplanet_table)
