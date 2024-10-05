import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
sns.set(style='dark')

# Load the dataset
all_df = pd.read_csv('all_df.csv')

st.title("Bike Rentals Dashboard")

# Sidebar filter
st.sidebar.header("Filter Options")

# filter for hour range 
hour_range = st.sidebar.slider('Select Hour Range of the Day', 0, 23, (6, 18))


# filter for season
season = st.sidebar.multiselect(
    'Select Season',
    [1, 2, 3, 4],
    format_func=lambda x: {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}[x],
    default=[1, 2, 3, 4] 
)

# filter for weather
weather = st.sidebar.multiselect(
    'Select Weather',
    [1, 2, 3],
    format_func=lambda x: {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain'}[x],
    default=[1, 2, 3]
)

# visualisasi 1
all_df = df[(df['hr'] >= hour_range[0]) & (df['hr'] <= hour_range[1])]

rentals_by_hour = all_df.groupby(by="hr").agg({"cnt": "mean"}).reset_index()

st.subheader(f"Average Rentals by Hour")
line_fig = px.line(rentals_by_hour, x='hr', y='cnt', labels={'cnt': 'Average Bike Rentals', 'hr': 'Hour of the Day'})
st.plotly_chart(line_fig)

# visualisasi 2
filtered_df = df[(df['season'].isin(season)) & (df['weathersit'].isin(weather))]

st.subheader(f"Bike Rental Counts by Seasons and Weather")
bar_data = filtered_df.groupby(['season', 'weathersit']).agg({'cnt': 'sum'}).reset_index()

season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain'}
bar_data['season'] = bar_data['season'].map(season_mapping)
bar_data['weathersit'] = bar_data['weathersit'].map(weather_mapping)

bar_fig = px.bar(bar_data, x='weathersit', y='cnt', color='season', labels={'cnt': 'Bike Rentals', 'weathersit': 'Weather'})
st.plotly_chart(bar_fig)
