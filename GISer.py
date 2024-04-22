import pandas as pd
import googlemaps
import json

# Function to load data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading the data: {e}")
        return None

# Function to consolidate address
def consolidate_address(row):
    try:
        return f"{row['ADDRESS']}, {row['CITY']}, {row['STATE']} {row['ZIP']}"
    except KeyError as e:
        print(f"Missing column in data: {e}")
        return None

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyCRfdzXBrBWPuFIpXmj_jTCepp6b3oJiGg')

# Function to geocode an address using Google Maps
def geocode_address(address):
    if not address:
        return None, None
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"No results found for {address}")
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

# Load the dataset
df = load_data('/Users/jacksonmiller/Desktop/School Mapping/GISMAP Scripts/SCHL_dataset.csv')
if df is None:
    raise Exception("Failed to load data.")

# Consolidate address components into a single column
df['Full_Address'] = df.apply(consolidate_address, axis=1)

# Apply geocoding
df['coords'] = df['Full_Address'].apply(geocode_address)

# Filter out rows where geocoding was not successful
df = df[df['coords'].apply(lambda x: x is not None and x != (None, None))]

# Check if the DataFrame is empty after filtering
if not df.empty:
    # Split the coordinates into latitude and longitude for easier access
    df[['Latitude', 'Longitude']] = pd.DataFrame(df['coords'].tolist(), index=df.index)

    # Create the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['Longitude'], row['Latitude']],
                },
                "properties": {
                    "school_id": row.get('IDOE_SCHOOL_ID', ''),
                    "school_name": row.get('SCHOOL_NAME', ''),
                    "principal": f"{row.get('PRINCIPAL_FIRST_NAME', '')} {row.get('PRINCIPAL_LAST_NAME', '')}",
                    "email": row.get('PRINCIPAL_EMAIL', ''),
                    "phone": row.get('PHONE', ''),
                    "address": row.get('ADDRESS', ''),
                    "city": row.get('CITY', ''),
                    "state": row.get('STATE', ''),
                    "zip": row.get('ZIP', ''),
                    "homepage": row.get('SCHOOL_HOMEPAGE', ''),
                    "choice_flag": row.get('CHOICE_FLAG', False)
                },
            } for idx, row in df.iterrows()
        ],
    }

    # Save the GeoJSON to a file
    with open('/Users/jacksonmiller/Desktop/School Mapping/GISMAP Scripts/SCHL_schools_geojson.geojson', 'w') as f:
        json.dump(geojson, f)
else:
    print("No valid geocoded results to create GeoJSON.")
