import streamlit as st


page_title = '太陽系外行星資料分析app'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)

st.info('此Web App是以太陽系外行星資料分析作為範例，用來教學及推廣公民科學，由[蘇羿豪](https://astrobackhacker.tw/)基於[Streamlit](https://streamlit.io/)開發，[程式碼](https://github.com/YihaoSu/ExoplanetDataAnalysisStreamlitUI)以MIT授權條款開源，並將開發過程紀錄在2022 iThome鐵人賽的系列文章「[跟著黑蛋用Streamlit速成天文資料分析Web App](https://ithelp.ithome.com.tw/users/20103436/ironman/5820)」中。')
st.markdown('* Exoplanet data intro頁面介紹何謂太陽系外行星，以及如何取得公開的太陽系外行星資料。')
st.markdown('* Exoplanet table filter頁面呈現從[NASA系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)取得的資料表，並提供資料篩選及匯出CSV檔的功能。')
st.markdown('* Exoplanet statistical charts頁面呈現系外行星資料的統計圖。')
st.markdown('* Exoplanet transit analysis頁面讓使用者能分析[Kepler太空望遠鏡](https://zh.wikipedia.org/zh-tw/%E5%85%8B%E5%8D%9C%E5%8B%92%E5%A4%AA%E7%A9%BA%E6%9C%9B%E9%81%A0%E9%8F%A1)及[凌日系外行星巡天衛星](https://zh.wikipedia.org/zh-tw/%E5%87%8C%E6%97%A5%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F%E5%B7%A1%E5%A4%A9%E8%A1%9B%E6%98%9F)的光變曲線觀測資料，以辨識出系外行星的凌日現象。')
