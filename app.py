# Day 6
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.set_page_config(
    page_title= "Superstore Dashboard",
    layout = "wide"
)

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQMqC_6fkaH6oZweJDIIYFDdE9o3P3G1hB0OKLzkGGf0pB-FjWJoAMoYca2iXV2ID5dE7hoklCSx6hE/pub?gid=0&single=true&output=csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

st.title("Superstore Dashboard")
st.dataframe(df)


df['order_year'] = df['order_date'].dt.year
CURR_YEAR = df['order_year'].max()
PREV_YEAR = CURR_YEAR - 1

mx_data = pd.pivot_table(
    data = df,
    index='order_year',
    aggfunc={
        'sales':np.sum,
        'profit':np.sum,
        'order_id':pd.Series.nunique,
        'customer_id':pd.Series.nunique
    }
).reset_index()

mx_data['profit_ratio'] = 100.0 * mx_data['profit']/ mx_data['sales']
mx_data
st.write('tes')

mx_sales, mx_order, mx_customer, mx_profit = st.columns(4)

with mx_sales:
    curr_sales = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'sales'].values[0]
    prev_sales = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'sales'].values[0]

    sales_diff_pct = 100.0 * (curr_sales - prev_sales)/ prev_sales

    st.metric(
        label='Sales',
        value=curr_sales,
        delta=f"{sales_diff_pct}%"
    )

with mx_order:
    curr_order = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'order_id'].values[0]
    prev_order = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'order_id'].values[0]

    order_diff_pct = 100.0 * (curr_order - prev_order)/ prev_order

    st.metric(
        label='Order',
        value=curr_order,
        delta=f"{order_diff_pct}%"
    )

with mx_customer:
    curr_customer = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'customer_id'].values[0]
    prev_customer = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'customer_id'].values[0]

    customer_diff_pct = 100.0 * (curr_customer - prev_customer)/ prev_customer

    st.metric(
        label='Customer',
        value=curr_customer,
        delta=f"{customer_diff_pct}%"
    )

with mx_profit:
    curr_profit = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'profit_ratio'].values[0]
    prev_profit = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'profit_ratio'].values[0]

    profit_diff_pct = curr_profit - prev_profit

    st.metric(
        label='Profit',
        value=curr_profit,
        delta=f"{profit_diff_pct}%"
    )


st.header("Sales")
sales_line = alt.Chart(df[df['order_year']== CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order date'),
    alt.Y('sales', title = 'Sales', aggregate='sum')
)

st.altair_chart(sales_line, use_container_width=True)

st.header("Sales")
sales_line = alt.Chart(df[df['order_year']== CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order date', timeUnit='yearmonth'),
    alt.Y('sales', title = 'Sales', aggregate='sum')
)

st.altair_chart(sales_line, use_container_width=True)


freqOption = st.selectbox(
    "Pilih frekuensi",
    options=("Harian","Bulanan")
)

timeUnit = {
    'Harian':'yearmonthdate',
    'Bulanan': 'yearmonth'
}

sales_custom = alt.Chart(df[df['order_year']== CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order date', timeUnit=timeUnit[freqOption]),
    alt.Y('sales', title = 'Sales', aggregate='sum')
)

st.altair_chart(sales_custom, use_container_width=True)


west, east, south, north = st.columns(4)
with west:
    st.header("West")
    sales_cat = alt.Chart(df[(df['order_year']== CURR_YEAR) & (df['region'] == 'West')]).mark_bar().encode(
        alt.X('category', title='Category', axis=alt.Axis(labelAngle=0)),
        alt.Y('sales', title = 'Sales', aggregate='sum')   
    )
# with east:
#     st.header("East")
# with south:
#     st.header("South")
# with north:
#     st.header("north")
    
st.altair_chart(sales_cat, use_container_width=True)


region_point = alt.Chart(df[df['order_year']== CURR_YEAR]).mark_point(filled=True).encode(
    alt.X('customer_id', aggregate='distinct'),
    alt.Y('order_id', aggregate='distinct'),
    color='region',
    size='sum(sales)'
)
st.altair_chart(region_point, use_container_width=True)
