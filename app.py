import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

df = pd.read_csv('vehicles_us.csv')
#df = df.drop(df.columns[0], axis=1)

# Fill missing model_year by grouping by model and using the median year
df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
# cylindres: group by model fill by median cylindres
df['cylinders'] = df.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))
# Function to safely calculate the median, returning a default value if all are NaN
def safe_median(series, default_value=np.nan):
    if series.isnull().all():
        return default_value
    else:
        return series.median()
#odometer: group by model year(or year+model) fill by median(mean) odometer
# Fill missing odometer by grouping by model_year and using the median odometer
df['odometer'] = df.groupby(['model', 'model_year'])['odometer'].transform(lambda x: x.fillna(safe_median(x)))
# If there are still missing values in odometer, fill them by grouping only by model
df['odometer'] = df.groupby('model')['odometer'].transform(lambda x: x.fillna(safe_median(x)))
# If there are still missing values in odometer, fill them by the overall median
global_median_odometer = df['odometer'].median()
df['odometer'] = df['odometer'].fillna(global_median_odometer)
#replace all nan in paimt_color with other.
df['paint_color'] = df['paint_color'].fillna('other')
#is_4wd fill in
g = df['is_4wd'].median()
df['is_4wd'] = df['is_4wd'].fillna(g)
#car's age
df.loc[:, 'age'] = 2024 - df.loc[:, 'model_year']
#clean  up model year and the odometer column by converting to int.64
df['model_year'] =df['model_year'].astype(int)
df['odometer'] =df['odometer'].astype(int)
#convert date_posted column to datetime format
df['date_posted'] = pd.to_datetime(df['date_posted'])
# split model column to create the first part of the string as the manufacturer and keep the sec part of the string as model.
df[['manufacturer', 'model']] = df['model'].str.split(' ', n=1, expand=True)
#move the manufacturer column to be close to the front of model to keep unison.


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

README.md
