import streamlit as st
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
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
    distance_column_name = f'與地球的距離(單位：{distance_unit})'
    exoplanet_table = exoplanet_table.rename(
        columns={'與地球的距離': distance_column_name}
    )

    return exoplanet_table, distance_column_name
