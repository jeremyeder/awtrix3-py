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