import requests
import csv
import io
import os

def get_session_data(year):
    # API endpoint
    url = "https://api.openf1.org/v1/sessions"
    
    # Query parameters for all sessions in the given year in CSV format
    params = {
        "year": year,
        "csv": "true"
    }
    
    try:
        # Make GET request
        response = requests.get(url, params=params)
        
        # Raise error if status code indicates failure
        response.raise_for_status()
        
        # Parse CSV response
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def get_stints_data(session_key, driver_number):
    # API endpoint for stints data in CSV format
    url = "https://api.openf1.org/v1/stints"
    
    # Query parameters for the driver
    params = {
        "driver_number": driver_number,
        "session_key": session_key,
        "csv": "true"
    }
    
    try:
        # Make GET request
        response = requests.get(url, params=params)
        
        # Raise error if status code indicates failure
        response.raise_for_status()
        
        # Parse CSV response
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stints data from API: {e}")
        return None

def get_weather_data(meeting_key):
    # API endpoint for weather data in CSV format
    url = "https://api.openf1.org/v1/weather"
    
    # Query parameters for the meeting
    params = {
        "meeting_key": meeting_key,
        "csv": "true"
    }
    
    try:
        # Make GET request
        response = requests.get(url, params=params)
        
        # Raise error if status code indicates failure
        response.raise_for_status()
        
        # Parse CSV response
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data from API: {e}")
        return None

def get_race_control_data(session_key):
    # API endpoint for race control data in CSV format
    url = "https://api.openf1.org/v1/race_control"
    
    # Query parameters for the session
    params = {
        "session_key": session_key,
        "csv": "true"
    }
    
    try:
        # Make GET request
        response = requests.get(url, params=params)
        
        # Raise error if status code indicates failure
        response.raise_for_status()
        
        # Parse CSV response
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching race control data from API: {e}")
        return None

def get_position_data(session_key, driver_number):
    # API endpoint for position data in CSV format
    url = "https://api.openf1.org/v1/position"
    
    # Query parameters for the driver
    params = {
        "session_key": session_key,
        "driver_number": driver_number,
        "csv": "true"
    }
    
    try:
        # Make GET request
        response = requests.get(url, params=params)
        
        # Raise error if status code indicates failure
        response.raise_for_status()
        
        # Parse CSV response
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching position data from API: {e}")
        return None

def get_pit_data(session_key, driver_number):
    # API endpoint for pit data in CSV format
    url = "https://api.openf1.org/v1/pit"
    
    # Query parameters for the driver
    params = {
        "session_key": session_key,
        "driver_number": driver_number,
        "csv": "true"
    }
    
    try:
        # Make GET request
        response = requests.get(url, params=params)
        
        # Raise error if status code indicates failure
        response.raise_for_status()
        
        # Parse CSV response
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching pit data from API: {e}")
        return None

def write_csv(data, folder, filename):
    # Create data directory if it doesn't exist
    folder_path = os.path.join("data", folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Write CSV data to a file in the data directory
    filepath = os.path.join(folder_path, filename)
    with open(filepath, mode='w', newline='') as file:
        file.write(data)
        print(f"Data written to {filepath}")

def process_all_sessions(year):
    # Get session data for all sessions in the given year
    session_data = get_session_data(year)
    if session_data:
        # Write session data to CSV file
        write_csv(session_data, "grand-prix", "session_data.csv")
        
        # Process each session in the session data
        csv_reader = csv.DictReader(io.StringIO(session_data))
        for row in csv_reader:
            session_key = row.get("session_key")
            meeting_key = row.get("meeting_key")
            session_name = row.get("session_name")
            country_name = row.get("country_name")
            
            if session_key and meeting_key:
                location_folder = os.path.join("grand-prix", country_name.lower().replace(" ", "_"))
                # Get list of all drivers
                drivers = [
                    {"name": "sainz", "driver_number": "55"},
                    {"name": "leclerc", "driver_number": "16"},
                    {"name": "norris", "driver_number": "4"},
                    {"name": "verstappen", "driver_number": "1"},
                    {"name": "piastri", "driver_number": "81"},
                    {"name": "hamilton", "driver_number": "44"},
                    {"name": "russell", "driver_number": "63"},
                    {"name": "perez", "driver_number": "11"},
                    {"name": "alonso", "driver_number": "14"},
                    {"name": "hulkenberg", "driver_number": "27"},
                    {"name": "stroll", "driver_number": "18"},
                    {"name": "tsunoda", "driver_number": "22"},
                    {"name": "albon", "driver_number": "23"},
                    {"name": "magnussen", "driver_number": "20"},
                    {"name": "gasly", "driver_number": "10"},
                    {"name": "colapinto", "driver_number": "43"},
                    {"name": "ocon", "driver_number": "31"},
                    {"name": "lawson", "driver_number": "30"},
                    {"name": "guanyu", "driver_number": "24"},
                    {"name": "bottas", "driver_number": "77"}
                ]
                
                for driver in drivers:
                    driver_name = driver["name"]
                    driver_number = driver["driver_number"]
                    driver_folder = os.path.join("drivers", driver_name, location_folder)
                    
                    # Get stints data for the driver
                    stints_data = get_stints_data(session_key, driver_number)
                    if stints_data:
                        # Write stints data to CSV file
                        write_csv(stints_data, driver_folder, f"stints_data_{session_name}.csv")
                    else:
                        print(f"Failed to retrieve stints data for {driver_name} in session {session_name}.")
                    
                    # Get position data for the driver
                    position_data = get_position_data(session_key, driver_number)
                    if position_data:
                        # Write position data to CSV file
                        write_csv(position_data, driver_folder, f"position_data_{session_name}.csv")
                    else:
                        print(f"Failed to retrieve position data for {driver_name} in session {session_name}.")
                    
                    # Get pit data for the driver
                    pit_data = get_pit_data(session_key, driver_number)
                    if pit_data:
                        # Write pit data to CSV file
                        write_csv(pit_data, driver_folder, f"pit_data_{session_name}.csv")
                    else:
                        print(f"Failed to retrieve pit data for {driver_name} in session {session_name}.")
                
                # Get weather data for the meeting
                weather_data = get_weather_data(meeting_key)
                if weather_data:
                    # Write weather data to CSV file
                    write_csv(weather_data, os.path.join(location_folder, "weather"), f"weather_data_{session_name}.csv")
                else:
                    print(f"Failed to retrieve weather data for session {session_name}.")
                
                # Get race control data for the session
                race_control_data = get_race_control_data(session_key)
                if race_control_data:
                    # Write race control data to CSV file
                    write_csv(race_control_data, os.path.join(location_folder, "race-control"), f"race_control_data_{session_name}.csv")
                else:
                    print(f"Failed to retrieve race control data for session {session_name}.")
            else:
                print("Session key or meeting key not found in session data.")
    else:
        print(f"Failed to retrieve session data for year {year}.")

def main():
    # Process all sessions for the year 2024
    process_all_sessions("2024")

if __name__ == "__main__":
    main()
