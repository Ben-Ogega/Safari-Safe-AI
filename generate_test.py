import pandas as pd
import numpy as np
import random

def generate_supply_route_leads(filename="kisumu_supply_route_leads.csv", num_leads=1000):
    # 1. Setup Sample Data
    names = ["John", "Sarah", "Ochieng", "Amina", "Kiptoo", "Maria", "Bakari", "Zainab", "Mutua", "Kamau", "Wekesa", "Anyango"]
    surnames = ["Otieno", "Kamau", "Anyango", "Mutua", "Wekesa", "Owolabi", "Juma", "Kiptoo"]
    
    # Realistic Kisumu Supply Route Waypoints
    waypoints = [
        {"name": "Kisumu Center", "lat": -0.0917, "lon": 34.7680},
        {"name": "Maseno", "lat": 0.0044, "lon": 34.5983},
        {"name": "Luanda", "lat": 0.0333, "lon": 34.5888},
        {"name": "Yala", "lat": 0.0970, "lon": 34.5380},
        {"name": "Ugunja", "lat": 0.1650, "lon": 34.3910},
        {"name": "Busia Border", "lat": 0.4608, "lon": 34.1115},
        {"name": "Ahero Junction", "lat": -0.1740, "lon": 34.9210},
        {"name": "Awasi", "lat": -0.1380, "lon": 35.0600},
        {"name": "Kericho", "lat": -0.3677, "lon": 35.2833},
        {"name": "Kiboswa", "lat": 0.0030, "lon": 34.7610},
        {"name": "Majengo", "lat": 0.0630, "lon": 34.7250},
        {"name": "Kakamega", "lat": 0.2842, "lon": 34.7523}
    ]
    
    data = []
    
    for i in range(num_leads):
        # Generate random lead profile
        customer = f"{random.choice(names)} {random.choice(surnames)}"
        spent = round(random.uniform(5000, 500000), 2)
        orders = random.randint(1, 50)
        dormancy = random.randint(10, 400)
        
        # Logic Change: Pick a real hub and add jitter (approx +/- 500m)
        waypoint = random.choice(waypoints)
        lat = waypoint['lat'] + random.uniform(-0.005, 0.005)
        lon = waypoint['lon'] + random.uniform(-0.005, 0.005)
        address = waypoint['name']
        
        data.append([customer, address, spent, orders, dormancy, lat, lon])

    # 2. Create DataFrame
    df = pd.DataFrame(data, columns=[
        'customer_name', 'address_column', 'total_spent', 
        'order_count', 'days_dormant', 'lat', 'lon'
    ])
    
    # 3. Save
    df.to_csv(filename, index=False)
    print(f"✅ Generated {num_leads} leads in {filename}")

if __name__ == "__main__":
    generate_supply_route_leads()