#!/usr/bin/python3
import requests
import yaml
import math
import time
import sys
from colorama import init, Fore
from change_light import change_light_color_and_brightness

# Initialize colorama
init(autoreset=True)

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

BRIDGE_IP = config['bridge_ip']
API_KEY = config['api_key']
AURORA_LIGHT_IDS = config['aurora_light_ids']
previous_kp_index = config.get('previous_kp_index', 0)  # Get the previous KP-Index, default to 0


# Function to fetch the aurora KP-Index value
def fetch_aurora_value():
    # Check if a command-line argument was provided
    if len(sys.argv) > 1:
        try:
            value = float(sys.argv[1])  # Convert the argument to a float
            return round(value)  # Round up and return as integer
        except ValueError:
            print(Fore.RED + "Invalid KP-Index value provided as argument. Fetching from API instead.")

    # If no valid argument was provided or an exception occurred, fetch from the API
    # Replace with your actual aurora API endpoint logic
    # response = requests.get('YOUR_AURORA_API_ENDPOINT')
    # value = response.json()['kp_index_value']
    # return math.ceil(value)
    return 1

def decide_hue_and_brightness(kp_index):
    if kp_index < 1:
        return (None, None)  # Pale green with low brightness
    elif kp_index == 1:
        return (25500, 50)  # Slightly brighter green
    elif kp_index == 2:
        return (25500, 100)  # Slightly brighter green
    elif kp_index == 3:
        return (25500, 200)  # Slightly brighter green
    elif kp_index == 4:
        return (0, 150)  # Red with medium brightness
    else:
        # Progressively brighter reds for KP 5-9
        brightness = int(
            min(150 + (kp_index - 4) * 25, 254))  # Convert to integer and ensure brightness doesn't exceed 254
        return (0, brightness)


def blink_light(light_id):
    """Blink the light twice quickly to indicate growth in KP-Index."""
    # Turn the light off
    requests.put(f'http://{BRIDGE_IP}/api/{API_KEY}/lights/{light_id}/state', json={'on': False})
    time.sleep(0.3)  # Duration of the light being off
    # Turn the light on
    requests.put(f'http://{BRIDGE_IP}/api/{API_KEY}/lights/{light_id}/state', json={'on': True})
    time.sleep(0.3)  # Duration of the light being on
    # Repeat for second blink
    requests.put(f'http://{BRIDGE_IP}/api/{API_KEY}/lights/{light_id}/state', json={'on': False})
    time.sleep(0.3)
    requests.put(f'http://{BRIDGE_IP}/api/{API_KEY}/lights/{light_id}/state', json={'on': True})


if __name__ == '__main__':
    kp_index = fetch_aurora_value()

    hue, brightness = decide_hue_and_brightness(kp_index)
    for light_id in AURORA_LIGHT_IDS:
        change_light_color_and_brightness(light_id, hue, brightness)

    # If the new KP-Index is higher than the previous one, blink the light(s)
    if kp_index > previous_kp_index:
        for light_id in AURORA_LIGHT_IDS:
            blink_light(light_id)

    # Update the previous KP-Index in the config.yaml file
    config['previous_kp_index'] = kp_index
    with open('config.yaml', 'w') as file:
        yaml.safe_dump(config, file)
