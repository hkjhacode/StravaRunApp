# ===== FILE: app/route_tracker.py =====
import metrics as metrics_module
from datetime import datetime

class RouteTracker:
    def __init__(self):
        self.route = []
        self.total_distance_km = 0
        self.current_speed = 0
        self.avg_speed = 0
        self.max_speed = 0
        self.speeds = []
    
    def reset(self):
        self.route = []
        self.total_distance_km = 0
        self.current_speed = 0
        self.avg_speed = 0
        self.max_speed = 0
        self.speeds = []
    
    def add_point(self, lat, lon):
        self.route.append({'lat': lat, 'lon': lon})
        
        if len(self.route) > 1:
            dist = metrics_module.haversine_distance(
                self.route[-2]['lat'], self.route[-2]['lon'],
                lat, lon
            )
            self.total_distance_km += dist
            
            # Speed in km/h (assuming 0.5s between updates)
            self.current_speed = dist * 7200
            self.speeds.append(self.current_speed)
            
            if self.current_speed > self.max_speed:
                self.max_speed = self.current_speed
            
            if self.speeds:
                self.avg_speed = sum(self.speeds) / len(self.speeds)

