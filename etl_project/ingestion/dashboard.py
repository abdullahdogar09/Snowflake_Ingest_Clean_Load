import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session

session = get_active_session()



df = session.sql("""
    SELECT COUNTRY, STATE, ZIP_CODE
    FROM MY_TABLE
    WHERE COOUNTRY IS NOT NULL AND COUNTRY != 'US' AND STATE IS NOT NULL AND ZIP_CODE IS NOT NULL
    LIMIT 20
""")