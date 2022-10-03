from turtle import title
import pandas as pd
import streamlit as st
import lightkurve as lk
from st_aggrid import AgGrid, GridOptionsBuilder


page_title = '系外行星凌日分析'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('用[Lightkurve](https://docs.lightkurve.org/)套件取得[Kepler太空望遠鏡](https://zh.wikipedia.org/zh-tw/%E5%85%8B%E5%8D%9C%E5%8B%92%E5%A4%AA%E7%A9%BA%E6%9C%9B%E9%81%A0%E9%8F%A1)及[凌日系外行星巡天衛星](https://zh.wikipedia.org/zh-tw/%E5%87%8C%E6%97%A5%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F%E5%B7%A1%E5%A4%A9%E8%A1%9B%E6%98%9F)對於某恆星的觀測資料，並藉由[Box Least Squares](https://docs.astropy.org/en/stable/timeseries/bls.html)演算法分析其光變曲線，辨識出系外行星的凌日現象。')

col1, col2 = st.columns(2)
with col1:
    exoplanet_name = st.text_input('輸入系外行星所屬恆星名稱')
with col2:
    mission = st.selectbox('選擇太空望遠鏡觀測任務', ['Kepler', 'K2', 'TESS'])

if exoplanet_name:
    with st.spinner('正在搜尋與此恆星相關的光變曲線資料，請稍候...'):
        search_result_table = lk.search_lightcurve(
            exoplanet_name, mission=mission
        )
    search_result_df = search_result_table.table.to_pandas()

    if not search_result_df.empty:
        search_result_df = search_result_df[['mission', 'year']]
        search_result_df = search_result_df.rename(
            columns={
                'mission': '觀測任務',
                'year': '觀測年份'
            }
        )
        st.text('勾選觀測任務以顯示相應的光變曲線圖並以Box Least Squares演算法分析出行星的軌道週期')
        gb = GridOptionsBuilder.from_dataframe(search_result_df)
        gb.configure_selection('single', use_checkbox=True)
        for col in search_result_df.columns.values.tolist():
            gb.configure_column(col, suppressMovable=True, suppressMenu=True)

        gridOptions = gb.build()
        grid_response = AgGrid(
            search_result_df,
            gridOptions=gridOptions,
            height=400,
            update_mode='selection_changed',
            theme='balham'
        )
        selected_lc = pd.DataFrame(grid_response['selected_rows'])

        if not selected_lc.empty:
            row_index = selected_lc['_selectedRowNodeInfo'].iloc[0].get('nodeRowIndex')
            with st.spinner('正在下載該筆光變曲線資料，請稍候...'):
                lc = search_result_table[row_index].download()
                periodogram = lc.to_periodogram('bls')
                orbital_period = periodogram.period_at_max_power.value

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f'{exoplanet_name}的光變曲線圖')
                    st.pyplot(lc.plot().figure)
                with col2:
                    st.subheader(f'Box Least Squares演算法求得power最大的週期為{orbital_period}天')
                    st.pyplot(periodogram.plot().figure)
                
                st.subheader(f'以{orbital_period}作為行星軌道週期所畫出的疊合光變曲線圖')
                st.pyplot(lc.fold(orbital_period).scatter(title='aa').figure)

    else:
        st.error('查無資料')
