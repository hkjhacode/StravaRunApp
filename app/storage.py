# ===== FILE: app/storage.py =====
import json
import os
from datetime import datetime

class Storage:
    def __init__(self, db_path='runs.json'):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump([], f)
    
    def save_run(self, run_data):
        runs = self.get_all_runs()
        run_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        runs.append(run_data)
        with open(self.db_path, 'w') as f:
            json.dump(runs, f, indent=2)
    
    def get_all_runs(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def get_today_runs(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return [r for r in self.get_all_runs() if r['date'].startswith(today)]
