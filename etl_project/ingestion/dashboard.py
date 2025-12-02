import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("📊 Interactive Dashboard on Companies Information")
st.write("This dashboard is created on Companies.csv data")

df = session.sql("""
    SELECT COUNTRY, STATE, ZIP_CODE
    FROM MY_TABLE
    WHERE COUNTRY IS NOT NULL AND STATE IS NOT NULL AND ZIP_CODE IS NOT NULL
    LIMIT 20
""").to_pandas()

country_list = df['COUNTRY'].unique().tolist()
selected_country = st.selectbox("Select COUNTRY", ["ALL"] + country_list)

if selected_country != "ALL":
    state_list = df[df['COUNTRY'] == selected_country]['STATE'].unique().tolist()
else:
    state_list = df['STATE'].unique().tolist()

selected_state = st.selectbox("Select STATE", ["ALL"] + state_list)

filtered_data = df.copy()

if selected_country != 'ALL':
    filtered_data = filtered_data[filtered_data['COUNTRY'] == selected_country]

if selected_state != 'ALL':
    filtered_data = filtered_data[filtered_data['STATE'] == selected_state]


