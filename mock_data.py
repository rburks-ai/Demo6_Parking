import pandas as pd

PARKING_DATA = [
    # ── Atlanta ──────────────────────────────────────────────────────────────
    {"id": 1,  "city": "Atlanta",      "area": "Downtown",       "name": "Peachtree Center Garage",      "lat": 33.7598, "lon": -84.3877, "price_per_hour": 4.00, "type": "Garage",     "spots_available": 42, "rating": 4.2, "open_24h": True,  "distance_mi": 0.2, "amenities": ["EV Charging", "Security", "Covered"]},
    {"id": 2,  "city": "Atlanta",      "area": "Downtown",       "name": "CNN Center Parking",           "lat": 33.7574, "lon": -84.3963, "price_per_hour": 5.50, "type": "Garage",     "spots_available": 18, "rating": 4.0, "open_24h": True,  "distance_mi": 0.5, "amenities": ["Security", "Covered"]},
    {"id": 3,  "city": "Atlanta",      "area": "Downtown",       "name": "Lot 27 - Marietta St",         "lat": 33.7562, "lon": -84.3940, "price_per_hour": 2.00, "type": "Lot",        "spots_available": 65, "rating": 3.5, "open_24h": False, "distance_mi": 0.7, "amenities": []},
    {"id": 4,  "city": "Atlanta",      "area": "Midtown",        "name": "Colony Square Parking",        "lat": 33.7840, "lon": -84.3838, "price_per_hour": 3.50, "type": "Garage",     "spots_available": 30, "rating": 4.5, "open_24h": True,  "distance_mi": 0.3, "amenities": ["EV Charging", "Covered", "Restrooms"]},
    {"id": 5,  "city": "Atlanta",      "area": "Midtown",        "name": "Arts Center MARTA Lot",        "lat": 33.7892, "lon": -84.3841, "price_per_hour": 2.50, "type": "Lot",        "spots_available": 80, "rating": 3.8, "open_24h": False, "distance_mi": 0.8, "amenities": ["Restrooms"]},
    {"id": 6,  "city": "Atlanta",      "area": "Buckhead",       "name": "Lenox Square Parking",         "lat": 33.8463, "lon": -84.3616, "price_per_hour": 3.00, "type": "Garage",     "spots_available": 200,"rating": 4.1, "open_24h": True,  "distance_mi": 0.1, "amenities": ["Security", "Covered", "EV Charging"]},
    {"id": 7,  "city": "Atlanta",      "area": "Buckhead",       "name": "Phipps Plaza Street Level",    "lat": 33.8480, "lon": -84.3628, "price_per_hour": 2.00, "type": "Lot",        "spots_available": 12, "rating": 3.2, "open_24h": False, "distance_mi": 0.4, "amenities": []},
    {"id": 8,  "city": "Atlanta",      "area": "Old Fourth Ward", "name": "Ponce City Market Deck",      "lat": 33.7726, "lon": -84.3668, "price_per_hour": 4.00, "type": "Garage",     "spots_available": 55, "rating": 4.6, "open_24h": True,  "distance_mi": 0.2, "amenities": ["EV Charging", "Security", "Covered", "Restrooms"]},

    # ── New York City ─────────────────────────────────────────────────────────
    {"id": 9,  "city": "New York",     "area": "Midtown Manhattan","name": "Icon Parking - 54th St",     "lat": 40.7590, "lon": -73.9845, "price_per_hour": 18.00,"type": "Garage",    "spots_available": 8,  "rating": 3.9, "open_24h": True,  "distance_mi": 0.1, "amenities": ["Security", "Covered", "Valet"]},
    {"id": 10, "city": "New York",     "area": "Midtown Manhattan","name": "QuickPark - 42nd St",        "lat": 40.7549, "lon": -73.9840, "price_per_hour": 15.00,"type": "Garage",    "spots_available": 22, "rating": 3.6, "open_24h": True,  "distance_mi": 0.3, "amenities": ["Security", "Covered"]},
    {"id": 11, "city": "New York",     "area": "Midtown Manhattan","name": "SP+ Garage - 7th Ave",       "lat": 40.7570, "lon": -73.9900, "price_per_hour": 12.00,"type": "Garage",    "spots_available": 0,  "rating": 3.7, "open_24h": False, "distance_mi": 0.5, "amenities": ["Covered"]},
    {"id": 12, "city": "New York",     "area": "Lower Manhattan", "name": "Pier 40 Parking",            "lat": 40.7296, "lon": -74.0134, "price_per_hour": 8.00, "type": "Garage",     "spots_available": 110,"rating": 4.0, "open_24h": True,  "distance_mi": 0.6, "amenities": ["Security", "EV Charging", "Restrooms"]},
    {"id": 13, "city": "New York",     "area": "Lower Manhattan", "name": "Battery Park City Lot",      "lat": 40.7108, "lon": -74.0172, "price_per_hour": 7.00, "type": "Lot",        "spots_available": 35, "rating": 3.5, "open_24h": False, "distance_mi": 0.9, "amenities": []},
    {"id": 14, "city": "New York",     "area": "Brooklyn",       "name": "DUMBO Parking - Front St",    "lat": 40.7034, "lon": -73.9889, "price_per_hour": 6.00, "type": "Garage",     "spots_available": 25, "rating": 4.3, "open_24h": False, "distance_mi": 0.4, "amenities": ["Security", "EV Charging"]},

    # ── Chicago ───────────────────────────────────────────────────────────────
    {"id": 15, "city": "Chicago",      "area": "The Loop",       "name": "Grant Park North Garage",      "lat": 41.8827, "lon": -87.6233, "price_per_hour": 7.00, "type": "Garage",     "spots_available": 90, "rating": 4.4, "open_24h": True,  "distance_mi": 0.2, "amenities": ["EV Charging", "Security", "Covered", "Restrooms"]},
    {"id": 16, "city": "Chicago",      "area": "The Loop",       "name": "Millennium Park Garage",       "lat": 41.8826, "lon": -87.6226, "price_per_hour": 9.00, "type": "Garage",     "spots_available": 45, "rating": 4.2, "open_24h": True,  "distance_mi": 0.1, "amenities": ["EV Charging", "Security", "Covered"]},
    {"id": 17, "city": "Chicago",      "area": "The Loop",       "name": "Madison-Wabash Lot",           "lat": 41.8818, "lon": -87.6262, "price_per_hour": 4.50, "type": "Lot",        "spots_available": 28, "rating": 3.3, "open_24h": False, "distance_mi": 0.6, "amenities": []},
    {"id": 18, "city": "Chicago",      "area": "River North",    "name": "900 N. Michigan Parking",      "lat": 41.8978, "lon": -87.6264, "price_per_hour": 6.00, "type": "Garage",     "spots_available": 60, "rating": 4.0, "open_24h": True,  "distance_mi": 0.3, "amenities": ["Security", "Covered"]},
    {"id": 19, "city": "Chicago",      "area": "Wicker Park",    "name": "Division St Lot",              "lat": 41.9038, "lon": -87.6773, "price_per_hour": 3.00, "type": "Lot",        "spots_available": 40, "rating": 3.6, "open_24h": False, "distance_mi": 0.5, "amenities": ["Restrooms"]},

    # ── Los Angeles ───────────────────────────────────────────────────────────
    {"id": 20, "city": "Los Angeles",  "area": "Downtown",       "name": "Pershing Square Garage",       "lat": 34.0484, "lon": -118.2530,"price_per_hour": 5.00, "type": "Garage",     "spots_available": 75, "rating": 3.8, "open_24h": True,  "distance_mi": 0.2, "amenities": ["Security", "EV Charging"]},
    {"id": 21, "city": "Los Angeles",  "area": "Downtown",       "name": "LA Live Parking",              "lat": 34.0430, "lon": -118.2673,"price_per_hour": 8.00, "type": "Garage",     "spots_available": 30, "rating": 4.1, "open_24h": True,  "distance_mi": 0.4, "amenities": ["Security", "Covered", "Valet"]},
    {"id": 22, "city": "Los Angeles",  "area": "Hollywood",      "name": "Hollywood & Highland Parking", "lat": 34.1016, "lon": -118.3398,"price_per_hour": 6.00, "type": "Garage",     "spots_available": 120,"rating": 4.0, "open_24h": True,  "distance_mi": 0.1, "amenities": ["Security", "Covered", "Restrooms"]},
    {"id": 23, "city": "Los Angeles",  "area": "Santa Monica",   "name": "Santa Monica Civic Lot 1",     "lat": 34.0195, "lon": -118.4912,"price_per_hour": 3.00, "type": "Lot",        "spots_available": 55, "rating": 3.9, "open_24h": False, "distance_mi": 0.3, "amenities": ["EV Charging"]},
    {"id": 24, "city": "Los Angeles",  "area": "Santa Monica",   "name": "Parking Structure 8",          "lat": 34.0178, "lon": -118.4930,"price_per_hour": 2.00, "type": "Garage",     "spots_available": 88, "rating": 3.5, "open_24h": False, "distance_mi": 0.6, "amenities": ["Covered"]},

    # ── Miami ─────────────────────────────────────────────────────────────────
    {"id": 25, "city": "Miami",        "area": "Downtown",       "name": "Bayside Marketplace Garage",   "lat": 25.7751, "lon": -80.1864, "price_per_hour": 5.00, "type": "Garage",     "spots_available": 50, "rating": 4.1, "open_24h": True,  "distance_mi": 0.2, "amenities": ["Security", "Covered", "EV Charging"]},
    {"id": 26, "city": "Miami",        "area": "Downtown",       "name": "Government Center Lot",        "lat": 25.7740, "lon": -80.1970, "price_per_hour": 2.50, "type": "Lot",        "spots_available": 100,"rating": 3.4, "open_24h": False, "distance_mi": 0.8, "amenities": []},
    {"id": 27, "city": "Miami",        "area": "South Beach",    "name": "7th St Parking Garage",        "lat": 25.7770, "lon": -80.1310, "price_per_hour": 7.00, "type": "Garage",     "spots_available": 15, "rating": 3.7, "open_24h": True,  "distance_mi": 0.3, "amenities": ["Security", "Covered"]},
    {"id": 28, "city": "Miami",        "area": "South Beach",    "name": "17th St Convention Lot",       "lat": 25.7902, "lon": -80.1340, "price_per_hour": 4.00, "type": "Lot",        "spots_available": 70, "rating": 3.9, "open_24h": False, "distance_mi": 0.5, "amenities": ["Restrooms"]},
    {"id": 29, "city": "Miami",        "area": "Brickell",       "name": "Brickell City Centre Parking", "lat": 25.7606, "lon": -80.1936, "price_per_hour": 6.00, "type": "Garage",     "spots_available": 40, "rating": 4.4, "open_24h": True,  "distance_mi": 0.1, "amenities": ["EV Charging", "Security", "Covered", "Valet"]},

    # ── Austin ────────────────────────────────────────────────────────────────
    {"id": 30, "city": "Austin",       "area": "Downtown",       "name": "Austin Convention Center Garage","lat":30.2637,"lon":-97.7405,  "price_per_hour": 3.00, "type": "Garage",     "spots_available": 85, "rating": 4.0, "open_24h": True,  "distance_mi": 0.2, "amenities": ["Security", "Covered", "EV Charging"]},
    {"id": 31, "city": "Austin",       "area": "Downtown",       "name": "Warehouse District Lot",       "lat": 30.2659, "lon": -97.7502, "price_per_hour": 1.50, "type": "Lot",        "spots_available": 60, "rating": 3.6, "open_24h": False, "distance_mi": 0.6, "amenities": []},
    {"id": 32, "city": "Austin",       "area": "6th Street",     "name": "6th & Red River Garage",       "lat": 30.2665, "lon": -97.7350, "price_per_hour": 4.00, "type": "Garage",     "spots_available": 20, "rating": 3.8, "open_24h": True,  "distance_mi": 0.3, "amenities": ["Security"]},
    {"id": 33, "city": "Austin",       "area": "South Congress", "name": "SoCo Surface Lot",             "lat": 30.2480, "lon": -97.7481, "price_per_hour": 2.00, "type": "Lot",        "spots_available": 45, "rating": 3.9, "open_24h": False, "distance_mi": 0.4, "amenities": ["EV Charging"]},
]

def get_dataframe():
    return pd.DataFrame(PARKING_DATA)

def get_cities():
    return sorted(get_dataframe()["city"].unique().tolist())

def get_areas(city):
    df = get_dataframe()
    return sorted(df[df["city"] == city]["area"].unique().tolist())

def filter_parking(city, area=None, max_price=None, parking_type=None,
                   available_only=False, open_24h=False, sort_by="price_per_hour"):
    df = get_dataframe()
    df = df[df["city"] == city]
    if area and area != "All Areas":
        df = df[df["area"] == area]
    if max_price is not None:
        df = df[df["price_per_hour"] <= max_price]
    if parking_type and parking_type != "All Types":
        df = df[df["type"] == parking_type]
    if available_only:
        df = df[df["spots_available"] > 0]
    if open_24h:
        df = df[df["open_24h"] == True]
    df = df.sort_values(sort_by, ascending=(sort_by != "rating"))
    return df.reset_index(drop=True)
