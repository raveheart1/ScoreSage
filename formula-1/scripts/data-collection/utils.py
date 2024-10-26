import requests
import os

def get_session_data(year):
    url = "https://api.openf1.org/v1/sessions"
    params = {"year": year, "csv": "true"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching session data from API: {e}")
        return None

def write_csv(data, folder, filename):
    folder_path = os.path.join("data", folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)
    with open(filepath, mode='w', newline='') as file:
        file.write(data)

drivers = [
    {"name": "sainz", "driver_number": "55"},
    {"name": "leclerc", "driver_number": "16"},
    # Add other drivers as needed
]


# usage
# from utils import get_session_data, write_csv, drivers
