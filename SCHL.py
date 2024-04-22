import pandas as pd
from geopy.geocoders import Nominatim
import json

# Function to load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to geocode an address
def geocode(address, geolocator):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# Load the dataset
df = load_data('/Users/jacksonmiller/Desktop/School Mapping/GISMAP Scripts/SCHL_dataset.csv')

# Initialize the geocoder
geolocator = Nominatim(user_agent="myGeoApp")

# Apply geocoding
df['coords'] = df['ADDRESS'].apply(lambda x: geocode(x, geolocator))

# Split the coordinates into latitude and longitude for easier access, if geocode was successful
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
                "school_id": row['IDOE_SCHOOL_ID'],
                "school_name": row['SCHOOL_NAME'],
                "principal": f"{row['PRINCIPAL_FIRST_NAME']} {row['PRINCIPAL_LAST_NAME']}",
                "email": row['PRINCIPAL_EMAIL'],
                "phone": row['PHONE'],
                "address": row['ADDRESS'],
                "city": row['CITY'],
                "state": row['STATE'],
                "zip": row['ZIP'],
                "homepage": row['SCHOOL_HOMEPAGE'],
                "choice_flag": row['CHOICE_FLAG']
            },
        } for idx, row in df.iterrows() if row['coords'] != (None, None)
    ],
}

# Save the GeoJSON to a file
with open('/users/jacksonmiller/Desktop/School Mapping/SCHL_schools_geojson.geojson', 'w') as f:
    json.dump(geojson, f)
