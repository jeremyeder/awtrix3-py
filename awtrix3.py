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
    
    def configure_settings(self, settings):
        """Update device settings"""
        response = requests.post(f"{self.base_url}/settings", json=settings, auth=self.auth)
        response.raise_for_status()
        return response.json() if response.text else None
    
    def clock_profile(self, format_24hr=True, show_seconds=False, minimal=True):
        """Configure device as a minimal clock
        
        Args:
            format_24hr (bool): Use 24-hour format, default True
            show_seconds (bool): Show seconds in time display, default False  
            minimal (bool): Strip down to minimal settings, default True
        """
        time_format = "HH:mm:ss" if show_seconds else "HH:mm"
        if not format_24hr:
            time_format = "hh:mm:ss A" if show_seconds else "hh:mm A"
        
        settings = {
            "timeFormat": time_format,
            "dateFormat": "",  # Disable date display for minimal clock
            "autoTransition": False,  # Disable app transitions
            "brightness": 80,  # Reasonable default brightness
            "transitionTime": 0,  # No transition delay
            "apps": []  # Disable all apps for minimal setup
        }
        
        if minimal:
            # Additional minimal settings to strip down the display
            settings.update({
                "showWeekday": False,
                "showClock": True,
                "showCalendar": False,
                "temperatureUnit": "",  # Disable temperature
                "batteryLevel": False,  # Disable battery display
                "scrollSpeed": 0  # No scrolling
            })
        
        return self.configure_settings(settings)