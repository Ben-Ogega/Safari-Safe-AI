import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def calculate_bridge_score(row, max_days):
    # Safety: avoid division by zero if all leads are new
    if max_days == 0: return 100.0
    r_score = 1 - (row['days_dormant'] / max_days)
    f_score = np.log1p(row['order_count']) / 5
    m_score = np.log1p(row['total_spent']) / 10
    return round(((r_score * 0.2) + (f_score * 0.4) + (m_score * 0.4)) * 100, 2)

def plan_cluster_visit(csv_path, radius_km=2.0):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Error: Could not find file at {csv_path}")
        return

    if df.empty:
        print("⚠️ The CSV file is empty.")
        return
    
    # 1. Scoring Logic
    max_d = df['days_dormant'].max()
    df['priority_score'] = df.apply(calculate_bridge_score, axis=1, max_days=max_d)
    
    # 2. Identify the Anchor
    df = df.sort_values(by='priority_score', ascending=False)
    anchor_lead = df.iloc[0]
    
    # 3. Radius Filtering
    df['dist_to_anchor'] = df.apply(
        lambda r: haversine(anchor_lead['lat'], anchor_lead['lon'], r['lat'], r['lon']), 
        axis=1
    )
    
    cluster = df[df['dist_to_anchor'] <= radius_km].copy().sort_values(by='dist_to_anchor')
    
    # --- 4. THE OUTPUT ---
    print(f"\n🎯 ANCHOR LEAD: {anchor_lead['customer_name']} (Score: {anchor_lead['priority_score']})")
    print("-" * 100)
    
    if len(cluster) <= 1:
        print(f"ℹ️ No other leads found within {radius_km}km.")
    else:
        print(f"🚀 VISIT ORDER (Within {radius_km}km of {anchor_lead['customer_name']}):")
        
        # Select and reorder columns for the exact view you want
        display_columns = [
            'customer_name', 'address_column', 'total_spent', 
            'order_count', 'days_dormant', 'lat', 'lon', 
            'priority_score', 'dist_to_anchor'
        ]
        
        # Using .to_string() makes it look like a neat table in your terminal
        print(cluster[display_columns].to_string(index=False))

if __name__ == "__main__":
    # Point this to your generated test file
    target_file = r"C:\Users\User\Desktop\FileOrganizer\test_leads.csv"
    plan_cluster_visit(target_file, radius_km=2.0)
