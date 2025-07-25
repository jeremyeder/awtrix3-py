import requests


class Awtrix3:
    def __init__(self, host, auth=None):
        self.base_url = f"http://{host}/api"
        self.auth = auth
    
    def notify(self, text):
        """Send a simple text notification"""
        data = {"text": text}
        response = requests.post(f"{self.base_url}/notify", json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def stats(self):
        """Get device statistics"""
        response = requests.get(f"{self.base_url}/stats", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def power(self, on=True):
        """Turn device on/off"""
        data = {"power": on}
        response = requests.post(f"{self.base_url}/power", json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def custom_app(self, name, text, **kwargs):
        """Create/update a custom app"""
        data = {"text": text, **kwargs}
        response = requests.post(f"{self.base_url}/custom", params={"name": name}, json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def play_sound(self, sound_name):
        """Play a sound by name"""
        data = {"sound": sound_name}
        response = requests.post(f"{self.base_url}/sound", json=data, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def delete_app(self, name):
        """Delete a custom app by name"""
        response = requests.delete(f"{self.base_url}/custom", params={"name": name}, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def list_apps(self):
        """Get list of apps currently in the loop"""
        response = requests.get(f"{self.base_url}/stats/loop", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_settings(self):
        """Get current device settings for backup"""
        response = requests.get(f"{self.base_url}/settings", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def backup_settings(self, filepath=None):
        """Backup device settings to JSON file
        
        Args:
            filepath (str): Path to save backup file. If None, returns settings dict.
            
        Returns:
            dict: Settings data if filepath is None
            str: Filepath where backup was saved if filepath provided
        """
        import json
        from datetime import datetime
        
        settings = self.get_settings()
        
        # Add metadata to backup
        backup_data = {
            "backup_timestamp": datetime.now().isoformat(),
            "backup_version": "1.0",
            "device_stats": self.stats(),
            "settings": settings
        }
        
        if filepath is None:
            return backup_data
            
        with open(filepath, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        return filepath
    
    def restore_settings(self, backup_data):
        """Restore device settings from backup data
        
        Args:
            backup_data (dict or str): Backup data dict or filepath to backup JSON
            
        Returns:
            dict: Result of settings update
        """
        import json
        
        if isinstance(backup_data, str):
            # Load from file
            with open(backup_data, 'r') as f:
                backup_data = json.load(f)
        
        if "settings" not in backup_data:
            raise ValueError("Invalid backup data: missing 'settings' key")
        
        settings = backup_data["settings"]
        
        # Apply settings using existing configure_settings method if available
        if hasattr(self, 'configure_settings'):
            return self.configure_settings(settings)
        else:
            # Fall back to direct API call
            response = requests.post(f"{self.base_url}/settings", json=settings, auth=self.auth)
            response.raise_for_status()
            return response.json() if response.text else None