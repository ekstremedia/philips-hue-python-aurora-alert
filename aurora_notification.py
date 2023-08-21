#!/usr/bin/python3
import requests
import yaml
import os
import time
import sys
from colorama import init, Fore
from change_light import change_light_color_and_brightness

# Initialize colorama
init(autoreset=True)

# Determine the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to config.yaml
config_file_path = os.path.join(script_directory, 'config.yaml')

# Load configuration from config.yaml
with open(config_file_path, 'r') as file:
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
            return round(value)  # Round to the nearest integer and return
        except ValueError:
            print(Fore.RED + "Invalid KP-Index value provided as argument. Fetching from API instead.")

    # Fetch from the API
    api_endpoint = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()  # Raise an HTTPError if an HTTP error occurred

        data = response.json()
        # Extract the KP-Index from the last entry
        last_entry = data[-1]
        kp_index = float(last_entry[1])  # KP-Index is the second element in each entry
        return round(kp_index)
    except requests.RequestException as e:
        print(Fore.RED + f"Failed to fetch KP-Index from API: {e}. Using previous value.")
        return previous_kp_index  # If there's an error, use the previously saved value


def decide_hue_and_brightness(kp_index):
    if kp_index < 1:
        return None, None  # Turn off the light
    elif kp_index == 1:
        return 45000, 50  # Light blue with low brightness
    elif kp_index == 2:
        return 25500, 100  # Pale green with medium brightness
    elif kp_index == 3:
        return 25500, 200  # Bright green
    elif kp_index == 4:
        return 0, 150  # Red with medium brightness
    elif kp_index == 5:
        return 0, 200  # Bright red
    elif kp_index == 6:
        return 50000, 200  # Pinkish-red
    elif kp_index == 7:
        return 55000, 150  # Purple with medium brightness
    else:
        return 55000, 254  # Deep purple with high brightness


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
