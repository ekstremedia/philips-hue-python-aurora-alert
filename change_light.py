#!/usr/bin/python3
import requests
import yaml
from colorama import init, Fore
import os

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
AURORA_LIGHT_IDS = config.get('aurora_light_ids', [])


def change_light_color_and_brightness(light_id, hue, brightness):
    """Change color (hue) and brightness of the specified light."""
    if hue is None and brightness is None:
        # Turn off the light
        data = {'on': False}
    else:
        data = {
            'on': True,  # Ensure the light is turned on
            'hue': hue,
            'bri': brightness,
        }

    response = requests.put(f'http://{BRIDGE_IP}/api/{API_KEY}/lights/{light_id}/state', json=data)

    response_data = response.json()

    # Check if response_data is a list and has at least one item
    if isinstance(response_data, list) and len(response_data) > 0:
        if "error" in response_data[0]:
            print(
                Fore.RED + f"Error changing light settings for light {light_id}: {response_data[0]['error']['description']}")
        else:
            print(Fore.GREEN + f"Successfully changed light settings for light {light_id}: {response_data}")
    else:
        # Print the entire response for debugging purposes
        print(Fore.RED + f"Unexpected response structure for light {light_id}: {response_data}")


def main():
    # Get light ID, hue, and brightness from the user
    light_id = input(Fore.YELLOW + "Enter the light ID: ")
    hue = int(input(Fore.YELLOW + "Enter the hue (0-65535): "))
    brightness = int(input(Fore.YELLOW + "Enter the brightness (0-254): "))

    # Change light color and brightness
    change_light_color_and_brightness(light_id, hue, brightness)


if __name__ == '__main__':
    main()
