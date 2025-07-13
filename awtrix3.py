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
    
    def get_settings(self):
        """Get current device settings"""
        response = requests.get(f"{self.base_url}/settings", auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def configure_settings(self, settings):
        """Configure device settings with provided JSON payload"""
        response = requests.post(f"{self.base_url}/settings", json=settings, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def clock_profile(self, format_24hr=True, show_seconds=False, minimal=True):
        """Configure device as a minimal clock with specified options
        
        Args:
            format_24hr (bool): Use 24-hour format (True) or 12-hour format (False)
            show_seconds (bool): Show seconds in time display
            minimal (bool): Strip down to minimal configuration (disable apps, weather, etc.)
        """
        # Base clock configuration
        time_format = "HH:mm:ss" if show_seconds else "HH:mm"
        if not format_24hr:
            time_format = "h:mm:ss A" if show_seconds else "h:mm A"
        
        settings = {
            "timeFormat": time_format,
            "show24hour": format_24hr
        }
        
        if minimal:
            # Strip down to minimal configuration - disable all non-essential features
            minimal_settings = {
                "autoTransition": False,
                "showWeekday": False,
                "showDate": False,
                "showHumidity": False,
                "showTemperature": False,
                "showBattery": False,
                "showWeather": False,
                "showApps": False,
                "brightness": 50,  # Moderate brightness
                "timeAppTime": 30,  # Show time for 30 seconds if apps are enabled
                "appTime": 7,  # Short app time
                "scrollSpeed": 100  # Reasonable scroll speed
            }
            settings.update(minimal_settings)
        
        return self.configure_settings(settings)