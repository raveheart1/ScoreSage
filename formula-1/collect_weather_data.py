import requests
import csv
import io
import os

def get_session_data(year):
    url = "https://api.openf1.org/v1/sessions"
    params = {
        "year": year,
        "csv": "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching session data from API: {e}")
        return None

def get_weather_data(meeting_key):
    url = "https://api.openf1.org/v1/weather"
    params = {
        "meeting_key": meeting_key,
        "csv": "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data from API: {e}")
        return None

def write_csv(data, folder, filename):
    folder_path = os.path.join("data", folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)
    with open(filepath, mode='w', newline='') as file:
        file.write(data)
        print(f"Weather data written to {filepath}")

def main():
    year = "2024"  # Change the year as needed
    session_data = get_session_data(year)
    if session_data:
        csv_reader = csv.DictReader(io.StringIO(session_data))
        for row in csv_reader:
            meeting_key = row.get("meeting_key")
            session_name = row.get("session_name")
            country_name = row.get("country_name")
            if meeting_key:
                location_folder = os.path.join("grand-prix", country_name.lower().replace(" ", "_"), "weather")
                weather_data = get_weather_data(meeting_key)
                if weather_data:
                    write_csv(weather_data, location_folder, f"weather_data_{session_name}.csv")
                else:
                    print(f"Failed to retrieve weather data for session {session_name}.")
    else:
        print(f"Failed to retrieve session data for year {year}.")

if __name__ == "__main__":
    main()
