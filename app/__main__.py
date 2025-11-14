#===== FILE: app/main.py =====
import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.popup import Popup

from gps_service import GPSService
from route_tracker import RouteTracker
from storage import Storage
from quotes import QuoteEngine
import metrics as metrics_module

Window.size = (540, 960)

class QuoteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quote_engine = QuoteEngine()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text="Today's Motivation", size_hint_y=0.15, font_size='28sp', bold=True)
        layout.add_widget(title)
        
        quote_data = self.quote_engine.get_daily_quote()
        quote_text = Label(
            text=quote_data['quote'],
            size_hint_y=0.5,
            font_size='18sp',
            text_size=(500, None),
            markup=True
        )
        layout.add_widget(quote_text)
        
        anime_name = Label(
            text=f"— {quote_data['anime']}",
            size_hint_y=0.2,
            font_size='14sp',
            color=(0.7, 0.7, 1, 1)
        )
        layout.add_widget(anime_name)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        btn_start = Button(text='Start Run', background_color=(0.2, 0.8, 0.3, 1))
        btn_history = Button(text='History', background_color=(0.3, 0.5, 0.9, 1))
        btn_start.bind(on_press=self.go_run)
        btn_history.bind(on_press=self.go_history)
        btn_layout.add_widget(btn_start)
        btn_layout.add_widget(btn_history)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def go_run(self, instance):
        self.manager.current = 'run'
    
    def go_history(self, instance):
        self.manager.current = 'history'


class RunScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gps_service = GPSService()
        self.route_tracker = RouteTracker()
        self.storage = Storage()
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_time = 0
        
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # GPS Status
        self.gps_status = Label(
            text="GPS: Connecting...",
            size_hint_y=0.08,
            font_size='12sp',
            color=(1, 1, 0, 1)
        )
        layout.add_widget(self.gps_status)
        
        # Metrics display
        self.metrics_label = Label(
            text="Distance: 0.00 km\nSpeed: 0.00 km/h\nTime: 00:00",
            size_hint_y=0.25,
            font_size='16sp',
            markup=True
        )
        layout.add_widget(self.metrics_label)
        
        # Coordinates display
        self.coords_label = Label(
            text="Lat: --\nLon: --\nAccuracy: -- m",
            size_hint_y=0.15,
            font_size='12sp'
        )
        layout.add_widget(self.coords_label)
        
        # Controls
        ctrl_layout = BoxLayout(size_hint_y=0.25, spacing=10)
        self.btn_start = Button(text='Start', background_color=(0.2, 0.8, 0.3, 1))
        self.btn_pause = Button(text='Pause', background_color=(1, 0.8, 0.2, 1), disabled=True)
        self.btn_stop = Button(text='Stop', background_color=(0.9, 0.2, 0.2, 1), disabled=True)
        self.btn_back = Button(text='Home', background_color=(0.5, 0.5, 0.5, 1))
        
        self.btn_start.bind(on_press=self.start_run)
        self.btn_pause.bind(on_press=self.pause_run)
        self.btn_stop.bind(on_press=self.stop_run)
        self.btn_back.bind(on_press=self.go_home)
        
        ctrl_layout.add_widget(self.btn_start)
        ctrl_layout.add_widget(self.btn_pause)
        ctrl_layout.add_widget(self.btn_stop)
        ctrl_layout.add_widget(self.btn_back)
        layout.add_widget(ctrl_layout)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Called when screen is shown"""
        self.gps_service.start_gps_listener()
        Clock.schedule_interval(self.check_gps_status, 1)
    
    def on_leave(self):
        """Called when leaving screen"""
        Clock.unschedule(self.check_gps_status)
        if self.running:
            self.stop_run(None)
    
    def check_gps_status(self, dt):
        """Check GPS connection status"""
        status = self.gps_service.get_status()
        if status['connected']:
            self.gps_status.text = f"GPS: Connected (Accuracy: {status['accuracy']:.0f}m)"
            self.gps_status.color = (0, 1, 0, 1)
        else:
            self.gps_status.text = "GPS: Searching..."
            self.gps_status.color = (1, 1, 0, 1)
    
    def start_run(self, instance):
        self.running = True
        self.paused = False
        self.start_time = Clock.get_time()
        self.pause_time = 0
        self.route_tracker.reset()
        self.btn_start.disabled = True
        self.btn_pause.disabled = False
        self.btn_stop.disabled = False
        Clock.schedule_interval(self.update_metrics, 0.5)
    
    def pause_run(self, instance):
        if self.paused:
            self.paused = False
            self.btn_pause.text = 'Pause'
            self.pause_time = 0
        else:
            self.paused = True
            self.btn_pause.text = 'Resume'
            self.pause_time = Clock.get_time()
    
    def stop_run(self, instance):
        self.running = False
        Clock.unschedule(self.update_metrics)
        
        if self.route_tracker.total_distance_km > 0:
            run_data = {
                'distance_km': self.route_tracker.total_distance_km,
                'duration_sec': int(Clock.get_time() - self.start_time - self.pause_time),
                'avg_speed_kmh': self.route_tracker.avg_speed,
                'max_speed_kmh': self.route_tracker.max_speed,
                'route': self.route_tracker.route,
                'points_count': len(self.route_tracker.route)
            }
            self.storage.save_run(run_data)
            self.metrics_label.text = f"✓ Run Saved!\nDistance: {self.route_tracker.total_distance_km:.2f} km\nDuration: {run_data['duration_sec']}s"
        else:
            self.metrics_label.text = "No distance recorded"
        
        self.btn_start.disabled = False
        self.btn_pause.disabled = True
        self.btn_stop.disabled = True
        self.paused = False
    
    def update_metrics(self, dt):
        if self.running and not self.paused:
            location = self.gps_service.get_latest_location()
            if location:
                self.route_tracker.add_point(location['lat'], location['lon'])
                
                elapsed = Clock.get_time() - self.start_time - self.pause_time
                
                self.metrics_label.text = (
                    f"Distance: {self.route_tracker.total_distance_km:.2f} km\n"
                    f"Speed: {self.route_tracker.current_speed:.2f} km/h\n"
                    f"Time: {int(elapsed // 60):02d}:{int(elapsed % 60):02d}"
                )
                
                self.coords_label.text = (
                    f"Lat: {location['lat']:.6f}\n"
                    f"Lon: {location['lon']:.6f}\n"
                    f"Accuracy: {location.get('accuracy', 0):.1f} m"
                )
    
    def go_home(self, instance):
        self.manager.current = 'quote'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = Storage()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='Run History', size_hint_y=0.1, font_size='24sp', bold=True)
        layout.add_widget(title)
        
        scroll = ScrollView(size_hint=(1, 0.8))
        self.runs_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.runs_layout.bind(minimum_height=self.runs_layout.setter('height'))
        
        scroll.add_widget(self.runs_layout)
        layout.add_widget(scroll)
        
        btn_back = Button(text='Back', size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1))
        btn_back.bind(on_press=self.go_home)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Refresh history when screen is shown"""
        self.runs_layout.clear_widgets()
        runs = self.storage.get_all_runs()
        
        if not runs:
            self.runs_layout.add_widget(Label(text='No runs yet!', size_hint_y=None, height=50))
        else:
            for run in reversed(runs):
                run_btn = Button(
                    text=(f"{run['date']} | "
                          f"{run['distance_km']:.2f}km | "
                          f"{run['avg_speed_kmh']:.2f}km/h | "
                          f"{run['points_count']} pts"),
                    size_hint_y=None,
                    height=50,
                    background_color=(0.3, 0.3, 0.5, 1)
                )
                self.runs_layout.add_widget(run_btn)
    
    def go_home(self, instance):
        self.manager.current = 'quote'


class StravaRunApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(QuoteScreen(name='quote'))
        sm.add_widget(RunScreen(name='run'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm


if __name__ == '__main__':
    StravaRunApp().run()
