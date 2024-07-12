#UPDATED CODE WITH APPLY FILTERS


import pandas as pd
import streamlit as st
import plotly.express as px
import requests

# Backend API URL
SALES_API_URL = "http://127.0.0.1:5000/api/sales"

# ---- FETCH DATA FROM API ----
@st.cache_data
def get_data_from_api(source='excel', gender=None, branch=None, city=None):
    params = {
        'source': source
    }
    if gender:
        params['Gender'] = gender
    if branch:
        params['Branch'] = branch
    if city:
        params['City'] = city

    response = requests.get(SALES_API_URL, params=params)
    
    if response.status_code == 200:
        print(pd.DataFrame(response.json()))
        return pd.DataFrame(response.json())
    else:
        st.error(f"Failed to fetch data from API. Status code: {response.status_code}")
        return pd.DataFrame()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

source = st.sidebar.selectbox(
    "Select Data Source:",
    options=["excel", "sql"],
    index=0
)

# Initial data fetch to populate filters
df = get_data_from_api(source=source)

city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique() if not df.empty else [],
    default=[]
)

branch = st.sidebar.multiselect(
    "Select the Branch:",
    options=df["Branch"].unique() if not df.empty else [],
    default=[]
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique() if not df.empty else [],
    default=[]
)

# Apply filters and fetch data
if st.sidebar.button("Apply Filters"):
    df_selection = get_data_from_api(
        source=source,
        gender=gender[0] if gender else None,
        branch=branch[0] if branch else None,
        city=city[0] if city else None
    )
else:
    df_selection = df

# Check if DataFrame is empty after filtering
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPIs
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"INR {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"INR {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Quantity"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY GENDER [BAR CHART]
sales_by_gender = df_selection.groupby(by=["Gender"])[["Total"]].sum()
fig_gender_sales = px.bar(
    sales_by_gender,
    x=sales_by_gender.index,
    y="Total",
    title="<b>Sales by Gender</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_gender),
    template="plotly_white",
)
fig_gender_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_gender_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
