import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import altair as alt
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

df = pd.read_csv('preprocessed_data_vehicles_us.csv')
df = df.drop(df.columns[0], axis=1)


st.title('Used Vehicles Listed for Sale')
st.header ('Vehicle Price Selector')
st.write ( 'Filter the used vehicles below to find cars of your interest based on manufacturer, model, transmission type, color, and price range.')

#filter by manufacturer
manufacturer = st.selectbox('Select Manufacturer', df['manufacturer'].unique())

filtered_data = df[df['manufacturer'] == manufacturer]

# Filter by model
model = st.selectbox('Select Model', filtered_data['model'].unique())

# Filter by transmission
transmission = st.selectbox('Select Transmission', filtered_data['transmission'].unique())

# Further filter data by selected transmission
filtered_data = filtered_data[filtered_data['transmission'] == transmission]

# Filter by paint color
paint_colors = st.multiselect('Select Paint Color(s)', filtered_data['paint_color'].unique(), default=filtered_data['paint_color'].unique())

# Further filter data by selected paint colors
filtered_data = filtered_data[filtered_data['paint_color'].isin(paint_colors)]

#create slider for selecting price range
min_price = int(filtered_data['price'].min())
max_price = int(filtered_data['price'].max())

#filter wusing slider for price range.
price_range = st.slider( "Select Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price) )
filtered_data = filtered_data[(filtered_data['price'] >= price_range[0]) & (filtered_data['price'] <= price_range[1])]
# Display filtered data
st.subheader("Filtered Cars")
st.dataframe(filtered_data)

#filter df based on the selected price range.
filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]





st.title('Odometer Vs.Price based on Manufacturer')
st.write('This scatter plot reflects the comparison between pricing, and the mileage of the odometer based on the listed manufacturer.')
fig = px.scatter(filtered_df, x="odometer", y="price", color="manufacturer", title="Odometer Readings vs. Price by Manufacturer")
st.plotly_chart(fig)


# Days listed in comparison to quantity listed per day.
st.title("Histogram of Days Listed")
st.write('Days listed in comparison to quantity listed per day.')

# Create histogram of days listed
fig = px.histogram(df, x="days_listed", title="Histogram of Days Listed")
st.plotly_chart(fig)