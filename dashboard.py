import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
from babel.numbers import format_currency
sns.set(style='dark')

def create_temperature_summary_df(df_hour):
    temperature_summary = df_hour[['temp', 'cnt']].describe()
    print("Ringkasan Statistik untuk Suhu dan Penyewaan Sepeda:\n", temperature_summary)
    return temperature_summary

def create_weekday_vs_weekend_summary_df(df_hour):
    weekday_vs_weekend_summary = df_hour.groupby('workingday')['cnt'].describe()
    print("Ringkasan Statistik untuk Penyewaan Sepeda pada Hari Kerja dan Hari Libur:\n", weekday_vs_weekend_summary)
    return weekday_vs_weekend_summary


all_df = pd.read_csv("https://github.com/fajarla/bike-sharing-dashboard/blob/main/hour.csv")

# Assuming all_df is your DataFrame and "dteday" is the date column
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# Convert min_date and max_date to datetime objects
min_date = datetime.strptime(min_date, "%Y-%m-%d")
max_date = datetime.strptime(max_date, "%Y-%m-%d")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/premium-vector/bike-icon-black-cycle-icon-bicycle-icon-mountain-bike-logo-vector-illustration_485380-696.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

st.header('Bike Sharing Dataset Dashboard :sparkles:')


daily_orders_df = create_temperature_summary_df(main_df)

# Create Daily Orders chart
daily_orders_df = main_df.groupby("dteday")["cnt"].sum().reset_index()

# Display metrics and chart
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df["cnt"].sum()
    st.metric("Total rental", value=total_orders)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticklabels(daily_orders_df["dteday"], rotation=45, ha="right")

st.pyplot(fig)


# Hitung ulang nilai temp berdasarkan rumus yang disediakan
t_min = -8
t_max = 39

# Hitung ulang suhu
all_df['recalculated_temp'] = (all_df['temp'] * (t_max - t_min)) + t_min

# Sidebar untuk memilih rentang suhu
st.sidebar.title("Rentang Suhu")
min_temp = st.sidebar.slider("Suhu Minimum", all_df['recalculated_temp'].min(), all_df['recalculated_temp'].max(), value=all_df['recalculated_temp'].min())
max_temp = st.sidebar.slider("Suhu Maksimum", all_df['recalculated_temp'].min(), all_df['recalculated_temp'].max(), value=all_df['recalculated_temp'].max())

# Filter data berdasarkan rentang suhu yang dipilih
filtered_df = all_df[(all_df['recalculated_temp'] >= min_temp) & (all_df['recalculated_temp'] <= max_temp)]

# Scatter plot untuk memvisualisasikan dampak suhu yang dihitung ulang pada penyewaan sepeda
st.title('Scatter Plot of Recalculated Temperature vs. Bike Rentals')
plt.figure(figsize=(10, 6))
scatter_plot = sns.scatterplot(x='recalculated_temp', y='cnt', data=filtered_df, hue='cnt', size='cnt', sizes=(20, 200))
plt.title('Scatter Plot of Recalculated Temperature vs. Bike Rentals')
plt.xlabel('Recalculated Temperature')
plt.ylabel('Count of Rental Bikes')
st.pyplot(plt)


# Sidebar untuk memilih jenis hari
st.sidebar.title("Pilih Jenis Hari")
selected_day_type = st.sidebar.radio("Jenis Hari:", ["Semua", "Hari Kerja", "Akhir Pekan"])

# Filter data berdasarkan jenis hari yang dipilih
if selected_day_type == "Hari Kerja":
    filtered_df = all_df[all_df['workingday'] == 1]
elif selected_day_type == "Akhir Pekan":
    filtered_df = all_df[all_df['workingday'] == 0]
else:
    filtered_df = all_df

# Boxplot untuk membandingkan penyewaan sepeda selama akhir pekan dan hari kerja
st.title('Boxplot of Bike Rentals on Working and Non-Working Days')
plt.figure(figsize=(12, 6))
box_plot = sns.boxplot(x='workingday', y='cnt', data=filtered_df)
plt.title('Boxplot of Bike Rentals on Working and Non-Working Days')
plt.xlabel('Working Day (1: Yes, 0: No)')
plt.ylabel('Count of Rental Bikes')
st.pyplot(plt)
