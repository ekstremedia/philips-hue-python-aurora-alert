#!/usr/bin/python3
import requests
import yaml
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

BRIDGE_IP = config['bridge_ip']
API_KEY = config['api_key']
LIGHT_ID = config['light_id']


def list_all_lights():
    """List all lights connected to the Hue Bridge in a table-like format."""
    response = requests.get(f'http://{BRIDGE_IP}/api/{API_KEY}/lights')
    lights = response.json()

    # Determine the maximum width needed for each column
    max_name_length = max(len(light_info['name']) for light_info in lights.values())
    max_type_length = max(len(light_info['type']) for light_info in lights.values())

    # Print the header
    print(Fore.YELLOW + f"{'ID':<5} {'Name':<{max_name_length}} {'Type':<{max_type_length}}")

    # Print each light's details
    for light_id, light_info in lights.items():
        print(
            Fore.BLUE + f"{light_id:<5} " + Fore.WHITE + f"{light_info['name']:<{max_name_length}} " + Fore.LIGHTBLACK_EX + f"{light_info['type']:<{max_type_length}}")


if __name__ == '__main__':
    # List all lights
    list_all_lights()
