import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Judul Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Membaca Dataset
df_day = pd.read_csv("Data/day.csv")

# Mengonversi kolom dteday ke datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Konversi data
df_day['season'] = df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df_day['weathersit'] = df_day['weathersit'].map({1: 'Clear', 2: 'Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'})
df_day['yr'] = df_day['yr'].map({0: '2011', 1: '2012'})
df_day.drop(columns=['instant'], inplace=True)
df_day['temp'] = df_day['temp'] * 41
df_day['hum'] = df_day['hum'] * 100
df_day['month'] = df_day['dteday'].dt.month
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_day['year'] = df_day['dteday'].dt.year

# Filter Berdasarkan Tanggal
st.sidebar.subheader("Filter Data")
start_date = st.sidebar.date_input("Pilih tanggal mulai", df_day['dteday'].min().date())
end_date = st.sidebar.date_input("Pilih tanggal akhir", df_day['dteday'].max().date())

# Filter Berdasarkan Musim & Cuaca
selected_season = st.sidebar.multiselect("Pilih Musim", df_day['season'].unique(), default=df_day['season'].unique())
selected_weather = st.sidebar.multiselect("Pilih Cuaca", df_day['weathersit'].unique(), default=df_day['weathersit'].unique())

# Menerapkan Filter
filtered_df = df_day[
    (df_day['dteday'] >= pd.to_datetime(start_date)) &
    (df_day['dteday'] <= pd.to_datetime(end_date)) &
    (df_day['season'].isin(selected_season)) &
    (df_day['weathersit'].isin(selected_weather))
]

# Visualisasi Pengaruh Cuaca terhadap Penyewaan
st.subheader("Penyewaan Sepeda Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df_day, x="weathersit", y="cnt", ax=ax, estimator=sum, ci=None)
ax.set_title("Total Penyewaan Sepeda Berdasarkan Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Penyewaan Sepeda")
st.pyplot(fig)

# Visualisasi Total Penyewaan Sepeda per Bulan
st.subheader("Total Penyewaan Sepeda per Bulan")
fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(data=filtered_df, x='month', y='cnt', hue='year', ax=ax, estimator=sum, ci=None, palette='viridis')
ax.set_title("Total Penyewaan Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_xticklabels(month_labels)  # Mengubah angka bulan menjadi nama bulan
st.pyplot(fig)