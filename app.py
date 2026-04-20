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
    # RFM-style scoring localized for heavy equipment leads
    r_score = 1 - (row['days_dormant'] / max_days)
    f_score = np.log1p(row['order_count']) / 5
    m_score = np.log1p(row['total_spent']) / 10
    return round(((r_score * 0.2) + (f_score * 0.4) + (m_score * 0.4)) * 100, 2)

# --- 2. GUI CONFIG & LIUGONG BRANDING ---
st.set_page_config(page_title="LiuGong Kenya | Lead Optimizer", layout="wide")

# Custom CSS for LiuGong 2026 Industrial Aesthetic
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    section[data-testid="stSidebar"] {
        background-color: #1C1C1C !important;
        border-right: 2px solid #FF8C00;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #FF8C00 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stSlider [data-baseweb="slider"] {
        background-color: #FF8C00;
    }
    section[data-testid="stFileUploadDropzone"] {
        border: 2px solid #FF8C00 !important;
        background-color: #1C1C1C;
    }
    div[data-testid="stMetric"] {
        background-color: #1C1C1C;
        border-left: 5px solid #FF8C00;
        border-radius: 4px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Branded Header [cite: 1, 4, 5]
st.title("🚜 LIUGONG KENYA: LEAD INTELLIGENCE")
st.subheader("922E & 933E Proximity Optimizer [Confidential • 2026]")
st.caption("Strategic Tool for Product Specialists | Optimized for Kenya & East Africa Market")

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("Settings")
radius = st.sidebar.slider("Search Radius (km)", 0.5, 15.0, 5.0)
uploaded_file = st.sidebar.file_uploader("Upload Lead Data (CSV)", type="csv", key="liugong_uploader")

# --- 4. LOGIC & RENDERING ---
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Verify Schema for 922E/933E Sales Targets [cite: 132, 186]
        required_cols = ['customer_name', 'days_dormant', 'order_count', 'total_spent', 'lat', 'lon']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            st.error(f"❌ Missing columns in CSV: {', '.join(missing)}")
            st.stop()

        # Scoring & Selection
        max_d = df['days_dormant'].max()
        df['priority_score'] = df.apply(calculate_bridge_score, axis=1, max_days=max_d)
        df = df.sort_values(by='priority_score', ascending=False)
        
        anchor = df.iloc[0] # The "High-Value" Target
        
        # Distance calculation relative to the Anchor
        df['km_away'] = df.apply(lambda r: haversine(anchor['lat'], anchor['lon'], r['lat'], r['lon']), axis=1)
        cluster = df[df['km_away'] <= radius].copy().sort_values(by='km_away')

        # --- 5. DASHBOARD LAYOUT ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"🗺️ Route Cluster: {anchor['customer_name']}")
            m = folium.Map(location=[anchor['lat'], anchor['lon']], zoom_start=13, tiles="CartoDB dark_matter")
            
            # Anchor Marker (Red Star)
            folium.Marker(
                [anchor['lat'], anchor['lon']], 
                popup=f"ANCHOR: {anchor['customer_name']} (Score: {anchor['priority_score']})",
                icon=folium.Icon(color='red', icon='star')
            ).add_to(m)
            
            # Cluster Markers (LiuGong Blue)
            for i, row in cluster.iloc[1:].iterrows():
                folium.Marker(
                    [row['lat'], row['lon']],
                    popup=f"{row['customer_name']} | {row['km_away']:.2f}km away",
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(m)
            
            st_folium(m, width=800, height=500)

        with col2:
            st.subheader("📊 Market Intelligence")
            st.metric("Cluster Size", f"{len(cluster)} Leads")
            st.metric("Avg. Priority Score", f"{round(cluster['priority_score'].mean(), 1)}%")
            
            st.write("---")
            st.write("**Top Leads in Radius:**")
            st.dataframe(
                cluster[['customer_name', 'priority_score', 'km_away']].head(10),
                use_container_width=True,
                hide_index=True
            )

        st.divider()
        st.subheader("🔍 Detailed Fleet Profiles")
        st.dataframe(cluster, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Systems Error: {e}")
else:
    st.info("👈 Upload the dealer's lead list to identify high-priority clusters for the 922E/933E excavator series.")