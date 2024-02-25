from geopy.distance import geodesic
from xml.dom.minidom import Document

# Function to calculate distance and flight time
def calculate_distance_and_flight_time(coord1, coord2, cruise_speed_knots):
    distance_nm = geodesic(coord1, coord2).nautical
    flight_time_hours = distance_nm / cruise_speed_knots
    return distance_nm, flight_time_hours

# Function to create KML file
def create_kml(airport_codes, coords):
    doc = Document()
    kml = doc.createElement('kml')
    kml.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
    doc.appendChild(kml)
    
    placemark = doc.createElement('Placemark')
    kml.appendChild(placemark)
    
    line_string = doc.createElement('LineString')
    placemark.appendChild(line_string)
    
    coordinates = doc.createElement('coordinates')
    
    for airport_code in airport_codes:
        coordinates.appendChild(doc.createTextNode(f"{coords[airport_code][1]}, {coords[airport_code][0]}, 0\n"))
    
    line_string.appendChild(coordinates)
    
    with open('flight_tour.kml', 'w') as file:
        file.write(doc.toprettyxml(indent="  "))

# Define coordinates for each airport
coords = {
    "SBRF": (-8.0476, -34.8770),
    "SBGR": (-23.4356, -46.4731),
    "SBGL": (-22.8090, -43.2506),
    "SBCT": (-25.5322, -49.1739),
    "SBPA": (-29.9939, -51.1711),
    "SBBR": (-15.8711, -47.9186),
    "SBBE": (-1.3838, -48.4783),
    "SBFZ": (-3.7761, -38.5323),
    "SBRJ": (-22.9109, -43.1632),
    "SBFN": (-5.7703, -35.8950),
    "SBKP": (-23.0074, -47.1345),
    "SBEG": (-3.0386, -60.0497),
    "SBFL": (-27.6703, -48.5519),
    "SBCF": (-19.6341, -43.9632),
    "SBSV": (-12.9086, -38.3220),
}

# Assume average cruising speed for an A320 in knots
cruise_speed_knots = 450

# Create a list of airport codes in the desired tour order
airport_codes = ["SBRF", "SBGR", "SBGL", "SBCT", "SBPA", "SBBR", "SBBE", "SBFZ", "SBRJ", "SBFN",
                 "SBKP", "SBEG", "SBFL", "SBCF", "SBSV"]

# Loop through the airport pairs to calculate distances and flight times
for i in range(len(airport_codes) - 1):
    start_airport = airport_codes[i]
    end_airport = airport_codes[i + 1]
    
    coord_start = coords[start_airport]
    coord_end = coords[end_airport]
    
    distance, flight_time = calculate_distance_and_flight_time(coord_start, coord_end, cruise_speed_knots)
    
    # Display information for each leg
    print(f"{i + 1}. {start_airport} to {end_airport}")
    print(f"   - Distance: {distance:.2f} NM")
    print(f"   - Flight Time: {flight_time:.2f} hours\n")

# Create KML file
create_kml(airport_codes, coords)
print("KML file created: flight_tour.kml")
