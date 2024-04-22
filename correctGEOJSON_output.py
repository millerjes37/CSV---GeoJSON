import json

# Path to the original GeoJSON file
input_file_path = '/Users/jacksonmiller/Desktop/School Mapping/GISMAP Scripts/SCHL_schools_geojson.geojson'
# Path where the corrected file will be saved
output_file_path = '/Users/jacksonmiller/Desktop/School Mapping/GISMAP Scripts/CorrectedGEO_Outputs/corrected_SCHL_file.geojson'

# Function to replace NaN with null in JSON data
def replace_nan_with_null(data):
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if value == "NaN":
                data[key] = None  # Replacing "NaN" with None (which will be converted to null in JSON)
            else:
                replace_nan_with_null(value)
    elif isinstance(data, list):
        for item in data:
            replace_nan_with_null(item)

# Read the original GeoJSON file
with open(input_file_path, 'r') as file:
    geojson_data = json.load(file)

# Replace NaN with null
replace_nan_with_null(geojson_data)

# Write the corrected data to a new file
with open(output_file_path, 'w') as file:
    json.dump(geojson_data, file, indent=4)  # Using an indent for better readability of the output file

print("The file has been corrected and saved as:", output_file_path)
