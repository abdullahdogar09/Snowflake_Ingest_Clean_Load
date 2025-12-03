import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session
import plotly.graph_objects as go

session = get_active_session()

st.title("📊 Interactive Dashboard on Companies Information")
st.write("This dashboard is created on Companies.csv data")

df = session.sql("""
    SELECT COUNTRY, STATE, ZIP_CODE, COMPANY_ID, COMPANY_SIZE
    FROM MY_TABLE
    WHERE COUNTRY IS NOT NULL 
        AND COUNTRY != 'US'
        AND STATE IS NOT NULL 
        AND ZIP_CODE IS NOT NULL
        AND COMPANY_ID IS NOT NULL
        AND COMPANY_SIZE IS NOT NULL
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

# For Waterfall Chart
waterfall_df = filtered_data.groupby("COMPANY_SIZE").agg(STATE_COUNT = ("STATE", 'count')).reset_index()

# ----------------------------------------------------------------------------------------------------------------
# Scatter Plot Code

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
# Column Chart Code

st.subheader("Column Chart - Companies in each Country")

fig_column = px.bar(
    company_df,
    x = 'COUNTRY',
    y = 'COMPANY_COUNT',
    text = 'COMPANY_COUNT',
    title = 'Total Companies in each country'
)

fig_column.update_traces(
    marker = dict(
        color = 'purple',
        line = dict(width = 1.5, color = 'black'),
        opacity = 0.8
    )
)

fig_column.update_layout(
    plot_bgcolor = 'lightpink'
)

st.plotly_chart(fig_column, use_container_width = True)

# -----------------------------------------------------------------------------------------------------------------
# Waterdall chart Code 

st.subheader("Waterfall Chart - States by Company Size")

waterfall_df = waterfall_df.sort_values("COMPANY_SIZE")

fig_waterfall = go.Figure(go.Waterfall(
    x = waterfall_df['COMPANY_SIZE'],
    y = waterfall_df['STATE_COUNT'],
    text = waterfall_df['STATE_COUNT'],
    textposition = "outside"  
))

fig_waterfall.update_layout(
    plot_bgcolor = 'lightgreen'
)

st.plotly_chart(fig_waterfall, use_container_width = True)

st.dataframe(filtered_data)



