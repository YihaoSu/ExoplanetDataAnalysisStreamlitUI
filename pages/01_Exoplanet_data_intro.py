import pandas as pd
import streamlit as st
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive


page_title = '太陽系外行星資料簡介'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)

st.header('什麼是太陽系外行星?')
st.info('水星、金星、地球、火星、木星、土星、天王星、海王星都是繞行太陽這個恆星的行星，而位於太陽系之外、不繞行太陽轉的行星，稱為[太陽系外行星](https://zh.wikipedia.org/zh-tw/%E5%A4%AA%E9%99%BD%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F)，也常簡稱為系外行星。')

st.header('可以從哪裡取得太陽系外行星的資料？')
st.subheader('1.NASA系外行星資料庫網站')
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

st.subheader('2.NASA系外行星資料庫的API')
st.info('NASA系外行星資料庫提供以呼叫API的方式回傳系外行星資料表，它是基於[Table Access Protocol(TAP)](https://www.ivoa.net/documents/TAP/)標準，其[說明頁面](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html)除了描述API的使用方法，也說明各資料表欄位所代表的意義。這個API是使用[Astronomical Data Query Language(ADQL)](https://www.ivoa.net/documents/ADQL/20180112/PR-ADQL-2.1-20180112.html)語法來查詢資料表並過濾欄位，該語法是基於SQL。')
api_example_code = '''
import pandas as pd

# 在API網址中用ADQL的select...from...語法，查詢能一行綜觀同個行星所有欄位值的資料表「Planetary Systems Composite Parameters」，並篩選所需欄位。
table_name = 'pscomppars'
columns = 'pl_name,hostname,sy_dist,pl_orbper,pl_bmasse,pl_rade,disc_year,discoverymethod'
nasa_exoplanet_archive_api = f'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+{columns}+from+{table_name}&format=csv'
exoplanet_table = pd.read_csv(nasa_exoplanet_archive_api)
'''
with st.expander('範例程式'):
	st.code(api_example_code, language='python')
	with st.echo():
		def get_exoplanet_table_by_nasa_api():
			table_name = 'pscomppars'
			columns = 'pl_name,hostname,sy_dist,pl_orbper,pl_bmasse,pl_rade,disc_year,discoverymethod'
			nasa_exoplanet_archive_api = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query='
			nasa_exoplanet_archive_api += f'select+{columns}+from+{table_name}&format=csv'
			exoplanet_table = pd.read_csv(nasa_exoplanet_archive_api)
			exoplanet_table = exoplanet_table.rename(
				columns={
					'pl_name': '行星名稱',
					'hostname': '所屬恆星名稱',
					'sy_dist': '與地球的距離(單位：秒差距)',
					'pl_orbper': '行星軌道週期(單位：天)',
					'pl_bmasse': '行星質量(單位：地球質量)',
					'pl_rade': '行星半徑(單位：地球半徑)',
					'disc_year': '發現年份',
					'discoverymethod': '發現方法'
				}
			)
			exoplanet_table.sort_values(
				by='發現年份', ascending=False, inplace=True, ignore_index=True
			)

			return exoplanet_table

	if st.button('執行get_exoplanet_table_by_nasa_api()並呈現系外行星資料表'):
		exoplanet_table = get_exoplanet_table_by_nasa_api()
		st.dataframe(exoplanet_table)

st.subheader('3.Astroquery套件')
st.info('[Astroquery](https://astroquery.readthedocs.io/)是一個用來查詢、取得天文資料的Python套件，它能針對不同天文資料庫服務，用統一的Python語法，以星體名稱、星體座標範圍或其它篩選條件，過濾出資料庫所屬資料。藉由Astroquery，可以取得同類型星體的參數統整資料表(例如：系外行星資料表)，或是特定星體在不同電磁波段的影像、光譜、時序等觀測資料。')
astroquery_example_code = '''
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

# 在query_criteria()中指定要取得哪個系外行星資料表的哪些欄位
table_name = 'pscomppars'
columns = 'pl_name,hostname,sy_dist,pl_orbper,pl_bmasse,pl_rade,disc_year,discoverymethod'
exoplanet_table = NasaExoplanetArchive.query_criteria(table=table_name, select=columns)
'''
with st.expander('範例程式'):
	st.code(astroquery_example_code, language='python')
	with st.echo():
		def get_exoplanet_table_by_astroquery():
			table_name = 'pscomppars'
			columns = 'pl_name,hostname,sy_dist,pl_orbper,pl_bmasse,pl_rade,disc_year,discoverymethod'
			exoplanet_table = NasaExoplanetArchive.query_criteria(
				table=table_name, select=columns
			)
			exoplanet_table = exoplanet_table.to_pandas()
			exoplanet_table = exoplanet_table.rename(
				columns={
					'pl_name': '行星名稱',
					'hostname': '所屬恆星名稱',
					'sy_dist': '與地球的距離(單位：秒差距)',
					'pl_orbper': '行星軌道週期(單位：天)',
					'pl_bmasse': '行星質量(單位：地球質量)',
					'pl_rade': '行星半徑(單位：地球半徑)',
					'disc_year': '發現年份',
					'discoverymethod': '發現方法'
				}
			)
			exoplanet_table.sort_values(
				by='發現年份', ascending=False, inplace=True, ignore_index=True
			)

			return exoplanet_table

	if st.button('執行get_exoplanet_table_by_astroquery()並呈現系外行星資料表'):
		exoplanet_table = get_exoplanet_table_by_astroquery()
		st.dataframe(exoplanet_table)

st.subheader('4.Lightkurve套件')
st.info('[Lightkurve](https://docs.lightkurve.org/)能尋找並下載[Kepler太空望遠鏡(Kepler/K2)](https://zh.wikipedia.org/zh-tw/%E5%85%8B%E5%8D%9C%E5%8B%92%E5%A4%AA%E7%A9%BA%E6%9C%9B%E9%81%A0%E9%8F%A1)及[凌日系外行星巡天衛星(TESS)](https://zh.wikipedia.org/zh-tw/%E5%87%8C%E6%97%A5%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F%E5%B7%A1%E5%A4%A9%E8%A1%9B%E6%98%9F)的觀測資料，且能將不同時段拍攝的影像資料轉換成[光變曲線](https://zh.wikipedia.org/zh-tw/%E5%85%89%E8%AE%8A%E6%9B%B2%E7%B7%9A)資料、計算光變週期，以[凌日法](https://zh.wikipedia.org/zh-tw/%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F%E5%81%B5%E6%B8%AC%E6%B3%95#%E5%87%8C%E6%97%A5%E6%B3%95)尋找太陽系外行星。')
lightkurve_example_code = '''
%matplotlib notebook
import lightkurve as lk

search_result_table = lk.search_lightcurve('系外行星所屬恆星名稱', mission='Kepler、K2或TESS')
lc = search_result_table[i].download() # i為search_result_table某一列的光變曲線資料
lc.plot()
'''
with st.expander('範例程式'):
	st.code(lightkurve_example_code, language='python')
