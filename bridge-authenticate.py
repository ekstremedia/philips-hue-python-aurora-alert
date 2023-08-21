#!/usr/bin/python3
import requests
import yaml
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def load_config():
    """Load configuration from config.yaml if it exists, otherwise return an empty dictionary."""
    try:
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}


def create_user(bridge_ip, device_type, computer_name):
    """Attempt to create a new user on the Hue Bridge."""
    data = {"devicetype": f"{device_type}#{computer_name}"}
    response = requests.post(f'http://{bridge_ip}/api', json=data)
    return response.json()


def main():
    config = load_config()

    # Retrieve or prompt for bridge_ip
    bridge_ip = config.get("bridge_ip")
    if bridge_ip:
        print(Fore.GREEN + f"Found Bridge IP in config.yaml: {bridge_ip}")
    else:
        bridge_ip = input(Fore.YELLOW + "Enter the IP address of your Hue Bridge: ")

    # Retrieve or prompt for device_type
    device_type = config.get("device_type")
    if device_type:
        print(Fore.GREEN + f"Found Device Type in config.yaml: {device_type}")
    else:
        device_type = input(Fore.YELLOW + "Enter the device type (e.g., HuePythonApp): ")

    # Retrieve or prompt for computer_name
    computer_name = config.get("computer_name")
    if computer_name:
        print(Fore.GREEN + f"Found Computer Name in config.yaml: {computer_name}")
    else:
        computer_name = input(Fore.YELLOW + "Enter the computer name (e.g., MyComputer): ")

    # Instruct user to press the link button on the Hue Bridge
    print(Fore.BLUE + "\nPlease press the link button on your Hue Bridge.")
    input("Press Enter to continue once you've pressed the button...")

    # Attempt to authenticate
    response_data = create_user(bridge_ip, device_type, computer_name)

    # Check for success
    if "success" in response_data[0]:
        api_key = response_data[0]["success"]["username"]
        print(Fore.GREEN + f"Successfully authenticated! API key: {api_key}")

        # Update and save to config.yaml
        config["bridge_ip"] = bridge_ip
        config["device_type"] = device_type
        config["computer_name"] = computer_name
        config["api_key"] = api_key
        with open("config.yaml", "w") as file:
            yaml.safe_dump(config, file)

        print(Fore.BLUE + "Configuration updated in config.yaml.")
    else:
        print(Fore.RED + f"Error: {response_data[0]['error']['description']}")


if __name__ == '__main__':
    main()
