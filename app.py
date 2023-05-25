# Day 6
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.set_page_config(
    page_title= "Superstore Dashboard",
    layout = "wide"
)

df = pd.read_csv('C:/Users/syahru/Desktop/Tetris Program/python learning/day 6/superstore.csv')
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





























# DAY 5
# import streamlit as st
# import lorem


# st.set_page_config(
#     'Baru Tau Streamlit Euy',
#     layout='wide'
# )
# st.write("Hello World")

# ''' TEKS TANPA MENGGUNAKAN st.write'''

# ''' lorem ipsum '''
# print("ok jek")
# ''' lorem ipsum 2'''

# # Menulis teks di streamlit

# "Lah bisa gini"  # Magic
# "_Ini juga Hello World_" # Markdown miring
# '## coba ini jadi apa ##'# header abis pager harus spasi dulu

# st.caption("malem malem gak bisa mikir")

# st.code('import streamlit as st')

# st.code('''
# import pandas as pd
# import streamlit as st #ini untuk memanggil package
# ''')

# # latex
# st.latex("ax^2 + bx + c = 0")
# st.caption("malem malem gak bisa mikir")


# # Belajar bikin widget
# ini_tombol = st.button('TEKAN TOMBOL INI DONG')

# ini_tombol

# saya_setuju = st.checkbox('Centang jika setuju')
# saya_setuju

# if saya_setuju:
#     st.write('Setuju belajar lagi')
# else:
#     st.write('ayo belajar')


# # Radio button = memilih salah satu opsi dari opsi yang ada ( multiple choice)
# buah_favorit = st.radio(
#     'pilih buah favorit kamu:',
#     ['apel', 'jambu', 'rujak']
# )
# buah_favorit

# makanan = st.selectbox(
#     'Pilih makanan yang diorder',
#     ['paket goceng', 'paket ceban', 'happy meal']
# )
# makanan

# belanjaan = st.multiselect(
#     'pilih belanjaan kalian',
#     ['terigu', 'kacang', 'gak punya duit']
# )
# belanjaan



# parameter_alpha = st.slider(
#     'Insert alpha value:',
#     min_value=0.0,
#     max_value=1.0,
#     step= 0.1,
#     value=0.5,
# )

# parameter_alpha

# ukuran_baju = st.select_slider(
#     'ukuran baju',
#     ['s', 'm', 'l']
# )
# ukuran_baju

# no_hp = st.number_input(
#     'masukan no. hp kalian:',
#     min_value=0,
#     max_value=9999999999999,
#     step=1
# )
# no_hp

# nama = st.text_input('masukkan nama kalian')

# komentar = st.text_area("masukan komentar anda")
# komentar

# tanggal_pilihan = st.date_input('Masukan tanggal lahir pilihan')

# jam_mulai =st.time_input("masukan jam")
# jam_mulai

# warna = st.color_picker('masukan warna')
# warna

# # masukan image, video, suara

# # countainer dan layouting

# # kolom

# col, col2, col3 = st.columns(3)

# with col:
#     st.write('ini kolom 1')

# with col2:
#     st.write('ini kolom 2')

# with col3:
#     st.write('ini kolom 3')

# col4, col5, col6 = st.columns(3)

# with col4:
#     lahir_saya = st.date_input('tgl lahir')

# with col5:
#     lahir_dia = st.date_input('tgl lahir dia')

# with col6:
#     kesimpulan = st.date_input('kesimpulan')
# st.button('hitung')


# with st.sidebar:
#     st.title('titanic survival model explorer')


