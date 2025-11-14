
# ===== FILE: app/metrics.py =====
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_speed(distance_km, time_seconds):
    """Calculate speed in km/h"""
    if time_seconds == 0:
        return 0
    return (distance_km / time_seconds) * 3600

def calculate_pace(speed_kmh):
    """Calculate pace in min/km"""
    if speed_kmh == 0:
        return 0
    return 60 / speed_kmh