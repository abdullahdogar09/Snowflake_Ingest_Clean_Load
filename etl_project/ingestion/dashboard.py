import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("📊 Interactive Dashboard on Companies Information")
st.write("This dashboard is created on Companies.csv data")

df = session.sql("""
    SELECT COUNTRY, STATE, ZIP_CODE, COMPANY_ID
    FROM MY_TABLE
    WHERE COUNTRY IS NOT NULL 
        AND STATE IS NOT NULL 
        AND ZIP_CODE IS NOT NULL
        AND COMPANY_ID IS NOT NULL
""").to_pandas()

country_list = sorted(df['COUNTRY'].unique().tolist())
selected_country = st.selectbox("Select COUNTRY", ["ALL"] + country_list)

if selected_country != "ALL":
    state_list = sorted(df[df['COUNTRY'] == selected_country]['STATE'].unique().tolist())
else:
    state_list = sorted(df['STATE'].unique().tolist())

selected_state = st.selectbox("Select STATE", ["ALL"] + state_list)

filtered_data = df.copy()

if selected_country != 'ALL':
    filtered_data = filtered_data[filtered_data['COUNTRY'] == selected_country]

if selected_state != 'ALL':
    filtered_data = filtered_data[filtered_data['STATE'] == selected_state]

# For Scatter Plot
zip_df = filtered_data.groupby("COUNTRY").agg(ZIP_CODE = ('ZIP_CODE', 'count')).reset_index()

# For Column Chart
company_df = filtered_data.groupby("COUNTRY").agg(COMPANY_COUNT = ('COMPANY_ID', 'count')).reset_index()

st.header("Scatter plot - Zip codes by Country")
# Scatter Plot Figure
fig_scatter = px.scatter(
    zip_df,
    x = 'COUNTRY',
    y = 'ZIP_CODE',
    size = 'ZIP_CODE',
    hover_name = 'COUNTRY',
    title = 'Total Zip Codes in each Country'
)

fig_scatter.update_traces(
    marker = dict(
        color = 'purple',
        line = dict(width = 1.5, color = 'black'),
        opacity = 0.8,
        symbol = 'square'
    )
)

# Scatter plot update layout
fig_scatter.update_layout(
    xaxis_title = 'Country',
    yaxis_title = 'Number of Zip Codes',
    template = 'plotly_white',
    plot_bgcolor = 'lightpink',
)

st.plotly_chart(fig_scatter, use_container_width = True)


# ------------------------------------------------------------------------------------------------------------

st.subheader("Column Chart - Companies in each Country")

fig_column = px.bar(
    company_df,
    x = 'COUNTRY',
    y = 'COMPANY_COUNT',
    text = 'COMPANY_COUNT',
    title = 'Total Companies in each country'
)

st.plotly_chart(fig_column, use_container_width = True)
st.dataframe(filtered_data)



