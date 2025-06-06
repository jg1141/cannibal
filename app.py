import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from folium.plugins import MarkerCluster

# Initialize session state for map data
if 'map_data' not in st.session_state:
    st.session_state.map_data = None
if 'clicked_location' not in st.session_state:
    st.session_state.clicked_location = None

# Set page config
st.set_page_config(page_title="Store Cannibalization Analysis", layout="wide")

# Title and description
st.title("Store Cannibalization Analysis")
st.markdown("""
This app helps visualize potential customer cannibalization when adding a new store location.
Drop a pin on the map to see which existing stores might be affected.
""")

# Sample existing store locations
EXISTING_STORES = {
    'Store 1': {'lat': 40.7128, 'lon': -74.0060},  # New York
    'Store 2': {'lat': 34.0522, 'lon': -118.2437},  # Los Angeles
    'Store 3': {'lat': 41.8781, 'lon': -87.6298},  # Chicago
    'Store 4': {'lat': 29.7604, 'lon': -95.3698},  # Houston
    'Store 5': {'lat': 39.9526, 'lon': -75.1652},  # Philadelphia
}

def create_map():
    # Create a map centered on the US
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add existing stores to the map
    marker_cluster = MarkerCluster().add_to(m)
    for store_name, coords in EXISTING_STORES.items():
        folium.Marker(
            location=[coords['lat'], coords['lon']],
            popup=store_name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)
    
    # If there's a clicked location, add it and show cannibalization areas
    if st.session_state.clicked_location:
        new_store_lat, new_store_lon = st.session_state.clicked_location
        
        # Add new store marker
        folium.Marker(
            location=[new_store_lat, new_store_lon],
            popup="New Store",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
        # Calculate and show cannibalization areas
        for store_name, coords in EXISTING_STORES.items():
            existing_store = (coords['lat'], coords['lon'])
            new_store = (new_store_lat, new_store_lon)
            
            distance = geodesic(new_store, existing_store).miles
            if distance < 50:  # 50 miles radius
                folium.Circle(
                    location=[coords['lat'], coords['lon']],
                    radius=distance * 1609.34,  # Convert miles to meters
                    color='red',
                    fill=True,
                    fill_opacity=0.2
                ).add_to(m)
    
    return m

# Create and display the map
m = create_map()
map_data = st_folium(m, width=800, height=600, returned_objects=["last_clicked"])

# Handle map clicks
if map_data and map_data["last_clicked"]:
    st.session_state.clicked_location = [
        map_data["last_clicked"]["lat"],
        map_data["last_clicked"]["lng"]
    ]
    st.rerun()

# Display results if there's a clicked location
if st.session_state.clicked_location:
    new_store_lat, new_store_lon = st.session_state.clicked_location
    
    # Calculate distances and determine cannibalization
    cannibalized_stores = []
    for store_name, coords in EXISTING_STORES.items():
        existing_store = (coords['lat'], coords['lon'])
        new_store = (new_store_lat, new_store_lon)
        
        distance = geodesic(new_store, existing_store).miles
        if distance < 50:
            cannibalized_stores.append({
                'store_name': store_name,
                'distance': round(distance, 2)
            })
    
    # Display results
    if cannibalized_stores:
        st.subheader("Potentially Cannibalized Stores:")
        df = pd.DataFrame(cannibalized_stores)
        st.dataframe(df)
    else:
        st.success("No significant cannibalization detected within 50 miles!")

# Add a button to clear the selection
if st.button("Clear Selection"):
    st.session_state.clicked_location = None
    st.rerun()

st.write("20250606 1500")