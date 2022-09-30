import streamlit as st
import plotly.express as px

from utilities import get_exoplanet_table_by_astroquery


def plot_piechart(exoplanet_table, column_name, title):
    fig = px.pie(
        exoplanet_table, names=column_name, color=column_name, title=title
    )

    return st.plotly_chart(fig, use_container_width=True)


def plot_histogram(exoplanet_table, column_name):
	fig = px.histogram(
        exoplanet_table, x=column_name, nbins=100,
    )
	fig.update_layout(
		yaxis_title='數量'
	)

	return st.plotly_chart(fig, use_container_width=True)


page_title = '系外行星資料統計圖'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('將系外行星資料表中的資料以統計圖呈現。')

with st.spinner('正在載入系外行星資料表，請稍候...'):
    exoplanet_table = get_exoplanet_table_by_astroquery()
    exoplanet_table = exoplanet_table.dropna()

col1, col2 = st.columns(2)
with col1:
    plot_piechart(exoplanet_table, '發現方法', '各種發現系外行星方法的佔比')

with col2:
    plot_piechart(
        exoplanet_table[exoplanet_table['發現方法'] == 'Transit'],
        '發現設施', '藉由凌日法(Transit)發現系外行星的地面天文台/太空望遠鏡佔比'
    )

column_name = st.radio(
    '切換直方圖要統計數量的欄位',
    ['發現年份', '行星質量(單位：地球質量)', '行星半徑(單位：地球半徑)', '行星軌道週期(單位：天)'],
    horizontal=True
)
plot_histogram(exoplanet_table, column_name)
