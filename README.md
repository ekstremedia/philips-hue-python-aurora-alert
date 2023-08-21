# Philips Hue Aurora KP-index based lighting 💡

Make specific lights get a color and brightness code based on current KP-index

Data from [NOAA Planetary Index](https://www.swpc.noaa.gov/products/planetary-k-index).

## Create and Activate a New Virtual Environment (optional, but recommended to avoid potential conflicts with system packages):

    python3 -m venv hue-env

#### On Linux/macOS
    source hue-env/bin/activate  
#### On Windows:

    hue-env\Scripts\activate

Install the Dependencies:

    pip install -r requirements.txt

## Set up config file

Copy example_config.yaml to config.yaml

    cp example_config.yaml config.yaml

Then edit it and add your Bridge's local ip to the `bridge_ip` key, or just run `bridge-authenticate.py` and enter the ip there.

### Authenticate with your bridge

    python3 bridge-authenticate.py

Withing 30 seconds, push the Bridge button, then return to the script and press enter

### List all your lights

    python3 list_lights.py

Add lights you want aurora notification for, in the `aurora_light_ids` [config.yaml](./example_config.yaml) setting

    aurora_light_ids:
    - 13
    - 7

### 

Change lights accordinging to data from NOAA's kpindex API

    python3 aurora_notification.py

To test with specific kp-index values, add a index as a parameter to see light change to this:

    python3 aurora_notification.py 3

Add this script to crontab to run every 5 minute:

    crontab -e

Add this rule, remember to edit the folder and environtment names

    */5 * * * * /home/pi/philips-hue-python-aurora-alert/hue-env/bin/python3 /home/pi/philips-hue-python-aurora-alert/aurora_notification.py >> /home/pi/philips-hue-python-aurora-alert/cron.log 2>&1

