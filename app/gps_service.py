# ===== FILE: app/gps_service.py =====
import os
import random
from datetime import datetime

class GPSService:
    def __init__(self):
        self.latest_location = {'lat': 40.7128, 'lon': -74.0060, 'accuracy': 10}
        self.gps_connected = False
        self.platform = self._detect_platform()
        self.gps_instance = None
    
    def _detect_platform(self):
        """Detect if running on Android"""
        if os.path.exists('/system/build.prop'):  # Android check
            return 'android'
        return 'desktop'
    
    def start_gps_listener(self):
        """Start GPS service"""
        if self.platform == 'android':
            self._start_android_gps()
        else:
            self._start_mock_gps()
    
    def _start_android_gps(self):
        """Start real GPS on Android using Plyer"""
        try:
            from plyer import gps
            self.gps_instance = gps
            
            def on_location(**kwargs):
                self.latest_location = {
                    'lat': kwargs.get('lat', 40.7128),
                    'lon': kwargs.get('lon', -74.0060),
                    'accuracy': kwargs.get('accuracy', 10)
                }
                self.gps_connected = True
            
            def on_status(sStatus):
                if sStatus == 'provider-enabled':
                    self.gps_connected = True
                else:
                    self.gps_connected = False
            
            gps.configure(on_location=on_location, on_status=on_status)
            gps.start(minTime=1000, minDistance=1)
        except Exception as e:
            print(f"Android GPS error: {e}")
            self._start_mock_gps()
    
    def _start_mock_gps(self):
        """Mock GPS for Windows/desktop testing"""
        self.gps_connected = True
    
    def get_latest_location(self):
        """Get current location"""
        if self.platform == 'desktop':
            # Mock GPS variation for testing
            self.latest_location['lat'] += random.uniform(-0.00005, 0.00005)
            self.latest_location['lon'] += random.uniform(-0.00005, 0.00005)
            self.latest_location['accuracy'] = random.uniform(5, 15)
        
        return self.latest_location
    
    def get_status(self):
        """Get GPS connection status"""
        return {
            'connected': self.gps_connected,
            'accuracy': self.latest_location.get('accuracy', 0),
            'platform': self.platform
        }

