import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from math import radians, cos, sin, asin, sqrt

# --- 1. CORE MATH ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def calculate_bridge_score(row, max_days):
    if max_days == 0: return 100.0
    r_score = 1 - (row['days_dormant'] / max_days)
    f_score = np.log1p(row['order_count']) / 5
    m_score = np.log1p(row['total_spent']) / 10
    return round(((r_score * 0.2) + (f_score * 0.4) + (m_score * 0.4)) * 100, 2)

# --- 2. GUI CONFIG ---
st.set_page_config(page_title="Safari-Safe Lead Optimizer", layout="wide")
st.title("📍 Lead Proximity Optimizer")

# Sidebar
st.sidebar.header("Settings")
radius = st.sidebar.slider("Search Radius (km)", 0.5, 10.0, 2.0)
uploaded_file = st.sidebar.file_uploader("Upload test_leads.csv", type="csv", key="main_loader")

# --- 3. LOGIC & RENDERING ---
if uploaded_file is not None:
    try:
        # Load and verify data
        df = pd.read_csv(uploaded_file)
        
        # Check for required columns to prevent silent crashes
        required_cols = ['customer_name', 'days_dormant', 'order_count', 'total_spent', 'lat', 'lon']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            st.error(f"❌ Missing columns in CSV: {', '.join(missing)}")
            st.stop()

        # Scoring Logic
        max_d = df['days_dormant'].max()
        df['priority_score'] = df.apply(calculate_bridge_score, axis=1, max_days=max_d)
        
        # Sort and pick the North Star (Anchor)
        df = df.sort_values(by='priority_score', ascending=False)
        anchor = df.iloc[0]
        
        # Calculate distance to anchor for everyone
        df['km_away'] = df.apply(lambda r: haversine(anchor['lat'], anchor['lon'], r['lat'], r['lon']), axis=1)
        
        # Filter the cluster
        cluster = df[df['km_away'] <= radius].copy().sort_values(by='km_away')

        # --- 4. DISPLAY COMPONENTS ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"🗺️ Route Map: {anchor['customer_name']}")
            # Create Map
            m = folium.Map(location=[anchor['lat'], anchor['lon']], zoom_start=14)
            
            # Anchor Marker
            folium.Marker(
                [anchor['lat'], anchor['lon']], 
                popup=f"ANCHOR: {anchor['customer_name']}",
                icon=folium.Icon(color='red', icon='star')
            ).add_to(m)
            
            # Cluster Markers
            for i, row in cluster.iloc[1:].iterrows():
                folium.Marker(
                    [row['lat'], row['lon']],
                    popup=f"{row['customer_name']} ({row['km_away']:.2f}km)",
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(m)
            
            st_folium(m, width=800, height=500)

        with col2:
            st.subheader("📋 Visit Priority")
            st.write(f"Showing **{len(cluster)}** leads within **{radius}km**.")
            st.dataframe(
                cluster[['customer_name', 'priority_score', 'km_away']],
                use_container_width=True
            )

        # Full Data Table at the bottom
        st.divider()
        st.subheader("🔍 Detailed Cluster Data")
        st.write(cluster)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
else:
    st.info("👈 Use the sidebar to upload your lead data and begin optimization.")