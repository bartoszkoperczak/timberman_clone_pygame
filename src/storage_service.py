import json
import os
from datetime import datetime


class StorageService:
    def __init__(self, data_dir="data"):
        """Initialize storage service and ensure data files exist."""
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, "history.json")
        self.config_file = os.path.join(data_dir, "config.json")
        os.makedirs(data_dir, exist_ok=True)
        self._init_files()

    def _init_files(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump({}, f)

    def add_history_record(self, record):
        """Add a new game record to the history file."""
        try:
            if 'timestamp' not in record:
                record['timestamp'] = datetime.now().isoformat()
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            history.append(record)
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            return True
        except Exception as e:
            print(f"Error adding history record: {e}")
            return False

    def get_all_history_records(self):
        """Return a list of all saved game history records."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading history records: {e}")
            return []

    def get_all_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading config: {e}")
            return {}

    def save_config_entry(self, key, value):
        try:
            config = self.get_all_config()
            config[key] = value
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config entry: {e}")
            return False

    def get_controls(self):
        """Get player controls from config or return defaults if not set."""
        config = self.get_all_config()
        return config.get("controls", {
            "player1": {"left": 97, "right": 100, "hit": 115},
            "player2": {"left": 1073741904, "right": 1073741903, "hit": 1073741905}
        })

    def save_controls(self, controls):
        """Save player controls to config file."""
        config = self.get_all_config()
        config["controls"] = controls
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

storage_service = StorageService()