######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static


######################
# Page Title
######################

# PIL.Image
image = Image.open('mosaic-logo.png')

#https://docs.streamlit.io/library/api-reference/media/st.image
st.image(image, use_column_width=False, width=400)




@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.title("Welcome to Mosaic Penthouse!")
st.markdown("""Mosaic Penthouses is a better way to book your stay in New York City. 
            Created in 2023 by Minh Pham as his final project for the class CIS-102,
            Mosaic Penthouses connects the people of need to the right homestay in New York City!""")
st.markdown("""### Learn about your options TODAY!""")
st.markdown("Here are some examples to get you started:")
st.dataframe(df.head(10))

st.markdown("""### Choose a location to start""")
boroughs = df['neighbourhood_group'].unique().tolist()
selected_borough = st.selectbox("New York Boroughs", boroughs, 0)

neighbourhoods = df[df['neighbourhood_group']==selected_borough]['neighbourhood'].unique().tolist()

selected_neighborhoods = st.multiselect("Neighborhood", neighbourhoods, default=neighbourhoods[0])

# st.dataframe(df[st_ms].head(10))

st.markdown("""### Choose your price range""")
prices = st.slider("Price range", float(df.price.min()), 1000., (50., 300.))
st.markdown(f"The price range is between \${prices[0]} and \${prices[1]}")

total = df[ 
    (df['neighbourhood_group']==selected_borough)
    & (df['neighbourhood'].isin(selected_neighborhoods))
    & (df['price'].between(prices[0], prices[1]))
    ]
st.markdown(f' Total {len(total)} housing rental are found in ${", ".join(selected_neighborhoods)}$ in {selected_borough} with price between \${prices[0]} and \${prices[1]}')

st.markdown("""### Map display""")
st.markdown("Click on the blue placemarks to learn more about each option")
# Get "latitude", "longitude", "price" for top listings

zoom_level = zoom_level = max(10, 14 - len(selected_neighborhoods))
init_lat = 40.7128
init_lon = -74.0060
if len(total) != 0:
    first_el = total.loc[total.index[0]]
    init_lat = first_el['latitude']
    init_lon = first_el['longitude']
m = folium.Map(location=[init_lat, init_lon], zoom_start=zoom_level)
for i in total.index:
    name, price, host_name, room_type = total['name'][i], total['price'][i], total['host_name'][i], total['room_type'][i]
    iframe_content = (
        f"""<div style='font-family: "Poppins"; font-size: 0.8rem'>
        {name}<br><br>
        Host Name: <strong>{host_name}</strong><br>
        Room Type: <strong>{room_type}</strong><br>
        Price: ${price}
        </div>"""
    )
    iframe = folium.IFrame(iframe_content, width=200, height=150)
    popup = folium.Popup(iframe, min_width=200, max_width=200)
    folium.Marker(
            location=[total['latitude'][i], total['longitude'][i]], 
            popup=popup,
            tooltip=f"${price}"
        ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)