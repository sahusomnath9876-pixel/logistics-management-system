from geopy.geocoders import Nominatim
import requests



def get_travel_data(city1, city2):
    # Initialize geolocator to convert city names to coordinates
    geolocator = Nominatim(user_agent="travel_calculator_project")
    
    loc1 = geolocator.geocode(city1)
    loc2 = geolocator.geocode(city2)
    
    if not loc1 or not loc2:
        return "One or both cities could not be found."
    
    # Extract coordinates (longitude, latitude order for OSRM API)
    coord1 = f"{loc1.longitude},{loc1.latitude}"
    coord2 = f"{loc2.longitude},{loc2.latitude}"
    
    # Call the free OpenStreetMap Routing API (OSRM)
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1};{coord2}?overview=false"
    response = requests.get(url, timeout=10).json()
    
    if response.get("code") != "Ok":
        return "Could not calculate a driving route between these locations."
        
    # Extract route summary data
    route = response["routes"][0]
    distance_km = route["distance"] / 1000  # Convert meters to km
    duration_mins = route["duration"] / 60  # Convert seconds to minutes
    
    return {
        "origin": loc1.address,
        "destination": loc2.address,
        "distance_km": round(distance_km, 2),
        "duration_mins": round(duration_mins, 1)
    }

