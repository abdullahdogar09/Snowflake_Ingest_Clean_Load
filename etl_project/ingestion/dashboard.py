import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# --- Title ---
st.title("📊 ZIP Code Distribution Dashboard")
st.write("Interactive Streamlit Dashboard with COUNTRY and STATE Filters")

# --- Load Data from Snowflake ---
df = session.sql("""
    SELECT COUNTRY, STATE, ZIP_CODE
    FROM MY_TABLE
    WHERE COUNTRY IS NOT NULL AND STATE IS NOT NULL AND ZIP_CODE IS NOT NULL AND COUNTRY != 'US'
    LIMIT 20
""").to_pandas()

# --- Slicers ---
country_list = df['COUNTRY'].unique().tolist()
selected_country = st.selectbox("Select COUNTRY", ["All"] + country_list)

# Filter states only from selected country
if selected_country != "All":
    state_list = df[df['COUNTRY'] == selected_country]['STATE'].unique().tolist()
else:
    state_list = df['STATE'].unique().tolist()

selected_state = st.selectbox("Select STATE", ["All"] + state_list)

# --- Apply Filtering ---
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df['COUNTRY'] == selected_country]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df['STATE'] == selected_state]

# --- Aggregation ---
plot_df = filtered_df.groupby('COUNTRY').agg(ZIP_COUNT=('ZIP_CODE', 'count')).reset_index()

# --- Visualization ---
fig = px.scatter(
    plot_df,
    x='COUNTRY',
    y='ZIP_COUNT',
    size='ZIP_COUNT',
    hover_name='COUNTRY',
    title='Country vs Number of ZIP Codes',
)

fig.update_layout(
    xaxis_title="Country",
    yaxis_title="Number of Zip Codes",
    title_x=0.5,
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

# --- Show Data (Optional) ---
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_df)
