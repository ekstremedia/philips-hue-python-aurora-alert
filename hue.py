#!/usr/bin/python3

import requests
import yaml

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

BRIDGE_IP = config['bridge_ip']
API_KEY = config['api_key']
LIGHT_ID = config['light_id']


def list_all_lights():
    """List all lights connected to the Hue Bridge."""
    response = requests.get(f'http://{BRIDGE_IP}/api/{API_KEY}/lights')
    lights = response.json()

    print("Available Lights:")
    for light_id, light_info in lights.items():
        print(f"{light_id}. {light_info['name']} - {light_info['type']}")


def change_light_color_and_brightness(hue, brightness):
    """Change color (hue) and brightness of the specified light."""
    data = {
        'hue': hue,  # 0-65535
        'bri': brightness,  # 0-254
    }
    response = requests.put(f'http://{BRIDGE_IP}/api/{API_KEY}/lights/{LIGHT_ID}/state', json=data)
    print(response.json())


if __name__ == '__main__':
    # Test the functions
    list_all_lights()
    change_light_color_and_brightness(40000, 200)
