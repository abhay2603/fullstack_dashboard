import pandas as pd
import plotly.express as px
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Function to load data from Excel
@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    try:
        df = pd.read_excel(
            io="supermarkt_sales.xlsx",
            engine="openpyxl",
            sheet_name="Sales",
            skiprows=0,  # Adjust skiprows if needed
            nrows=100,  # Adjust nrows if needed
        )
        
        # Check if 'Time' column exists in the dataframe
        if 'Time' in df.columns:
            df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.time
        else:
            st.error("Error: 'Time' column not found in the Excel data.")
            st.stop()  # Stop execution if 'Time' column is missing
        
        return df
    
    except FileNotFoundError:
        st.error("Error: File 'supermarkt_sales.xlsx' not found.")
        st.stop()  # Stop execution if file is not found
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()  # Stop execution for any other unexpected errors

# Load data from Excel
df = get_data_from_excel()

# Sidebar filters
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer type"].unique(),
    default=df["Customer type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Contact", "Settings"])

# Filter dataframe based on sidebar selections
# Ensure correct column names and string formatting in query
query_string = f"`City` == {city} and `Customer type` == {customer_type} and `Gender` == {gender}"
df_selection = df.query(query_string)

# Check if filtered dataframe is empty
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  # Stop execution if filtered dataframe is empty

# Main page content
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# Top KPIs
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# Display top KPIs in columns
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

# Separator line
st.markdown("""---""")

# Sales by Product Line (Bar chart)
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
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
    xaxis=dict(showgrid=False)
)

# Sales by Hour (Bar chart)
sales_by_hour = df_selection.groupby(by=["Time"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False),
)

# Display charts in two columns
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# Hide Streamlit style (optional)
# hide_st_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: show;}
# </style>
# """
# st.markdown(hide_st_style, unsafe_allow_html=True)
