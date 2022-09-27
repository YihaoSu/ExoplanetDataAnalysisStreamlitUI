import streamlit as st
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import astropy.units as u


@st.experimental_memo(ttl=86400, show_spinner=False)
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
            'sy_dist': '與地球的距離',
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


def get_distance_unit_dict():
    parsec = 1 * u.parsec
    parsec_to_lightyear = parsec.to(u.lyr)
    parsec_to_au = parsec.to(u.au)
    parsec_to_km = parsec.to(u.km)
    distance_unit_dict = {
        '秒差距': parsec,
        '光年': parsec_to_lightyear,
        '天文單位': parsec_to_au,
        '公里': parsec_to_km
    }

    return distance_unit_dict

def convert_exoplanet_table_distance_unit(
    exoplanet_table, distance_unit_dict, distance_unit
):
    exoplanet_table['與地球的距離'] = exoplanet_table[
        '與地球的距離'] * distance_unit_dict.get(distance_unit).value
    exoplanet_table = exoplanet_table.rename(
        columns={'與地球的距離': f'與地球的距離(單位：{distance_unit})'}
    )

    return exoplanet_table


page_title = '系外行星資料表篩選器'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('藉由[Astroquery](https://astroquery.readthedocs.io/en/latest/ipac/nexsci/nasa_exoplanet_archive.html)套件取得[NASA系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)提供的資料表，篩選出所需資料後匯出CSV檔。點擊表格中的行星名稱連結，可到NASA的[Eyes on Exoplanets](https://exoplanets.nasa.gov/eyes-on-exoplanets)網站瞧瞧它們在藝術家的眼中長得如何。')

with st.spinner('正在載入系外行星資料表，請稍候...'):
    exoplanet_table = get_exoplanet_table_by_astroquery()

distance_unit_dict = get_distance_unit_dict()
distance_unit = st.radio(
    '切換表格中的距離單位', list(distance_unit_dict.keys()), horizontal=True
)
exoplanet_table = convert_exoplanet_table_distance_unit(
    exoplanet_table, distance_unit_dict, distance_unit
)

with st.expander('各距離單位的換算'):
    st.markdown('[秒差距](https://zh.wikipedia.org/zh-tw/%E7%A7%92%E5%B7%AE%E8%B7%9D)、[光年](https://zh.wikipedia.org/zh-tw/%E5%85%89%E5%B9%B4)和[天文單位](https://zh.wikipedia.org/zh-tw/%E5%A4%A9%E6%96%87%E5%96%AE%E4%BD%8D)都是常用來描述星體距離的長度單位')
    st.markdown('1秒差距約為 $3.09*10^{13}$ 公里')
    st.markdown('1光年約為 $9.46*10^{12}$ 公里')
    st.markdown('1天文單位是地球和太陽的平均距離，約為 $1.5*10^{8}$ 公里')

year_min = int(exoplanet_table['發現年份'].min())
year_max = int(exoplanet_table['發現年份'].max())
year_lst = list(range(year_min, year_max + 1))
year_range = st.sidebar.select_slider(
    '篩選某年份區間內被發現的行星',
    options=year_lst,
    value=(year_min, year_max), 
)
exoplanet_table = exoplanet_table[
    (exoplanet_table['發現年份'] >= year_range[0]) &
    (exoplanet_table['發現年份'] <= year_range[1])
]

method_lst = sorted(list(exoplanet_table['發現方法'].unique()))
selected_method = st.sidebar.selectbox(
    '篩選被某個方法發現的行星', ['不限'] + method_lst
)
if selected_method != '不限':
    exoplanet_table = exoplanet_table[exoplanet_table['發現方法'] == selected_method]

column_name_lst = list(exoplanet_table.columns)
selected_columns = st.sidebar.multiselect(
    '去除某幾個欄位值為空值的行星', column_name_lst
)
exoplanet_table = exoplanet_table.dropna(subset=selected_columns)
exoplanet_table = exoplanet_table.reset_index(drop=True)

gb = GridOptionsBuilder.from_dataframe(exoplanet_table)
gb.configure_column('行星名稱', pinned='left')
gb.configure_column(
    '行星名稱',
    cellRenderer=JsCode('''
    function(params) {
        return '<a href="https://exoplanets.nasa.gov/eyes-on-exoplanets/#/planet/' + params.value.replaceAll(" ", "_") + '" target="_blank">' + params.value + '</a>'
    };
    ''')
)
for col in exoplanet_table.columns.values.tolist():
    gb.configure_column(col, suppressMovable=True, suppressMenu=True)

gridOptions = gb.build()
AgGrid(
    exoplanet_table,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True,
    height=400,
    theme='balham'
)

st.sidebar.download_button(
    label='將篩選資料表匯出成CSV檔',
    data=exoplanet_table.to_csv(index=False),
    file_name='exoplanet_table.csv',
    mime='text/csv'
)

if st.sidebar.button('清除資料表快取'):
    st.experimental_memo.clear()
    st.balloons()
    st.sidebar.success('已清除快取，請重新載入頁面')
