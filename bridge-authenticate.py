#!/usr/bin/python3
import requests
import yaml


def load_config():
    """Load configuration from config.yaml if it exists, otherwise return an empty dictionary."""
    try:
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}


def create_user(bridge_ip):
    """Attempt to create a new user on the Hue Bridge."""
    data = {"devicetype": "HuePythonApp#MyComputer"}
    response = requests.post(f'http://{bridge_ip}/api', json=data)

    return response.json()


def main():
    # Load bridge_ip from config.yaml if it exists, otherwise prompt for it
    config = load_config()
    bridge_ip = config.get("bridge_ip")
    if not bridge_ip:
        bridge_ip = input("Enter the IP address of your Hue Bridge: ")

    # Instruct user to press the link button on the Hue Bridge
    print(f"Using Bridge IP: {bridge_ip}")
    print("\nPlease press the link button on your Hue Bridge.")
    input("Press Enter to continue once you've pressed the button...")

    # Attempt to authenticate
    response_data = create_user(bridge_ip)

    # Check for success
    if "success" in response_data[0]:
        api_key = response_data[0]["success"]["username"]
        print(f"Successfully authenticated! API key: {api_key}")

        # Update and save to config.yaml
        config["bridge_ip"] = bridge_ip
        config["api_key"] = api_key
        with open("config.yaml", "w") as file:
            yaml.safe_dump(config, file)

        print("Configuration updated in config.yaml.")
    else:
        print(f"Error: {response_data[0]['error']['description']}")


if __name__ == '__main__':
    main()
