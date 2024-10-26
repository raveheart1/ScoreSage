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

def get_intervals_data(session_key):
    url = "https://api.openf1.org/v1/intervals"
    params = {
        "session_key": session_key,
        "csv": "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching intervals data from API: {e}")
        return None

def write_csv(data, folder, filename):
    folder_path = os.path.join("data", folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)
    with open(filepath, mode='w', newline='') as file:
        file.write(data)
    print(f"Data written to {filepath}")

def main():
    year = "2024"  # Change the year as needed
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
    session_data = get_session_data(year)
    if session_data:
        csv_reader = csv.DictReader(io.StringIO(session_data))
        for row in csv_reader:
            session_key = row.get("session_key")
            session_name = row.get("session_name")
            country_name = row.get("country_name")
            if session_key:
                location_folder = os.path.join("grand-prix", country_name.lower().replace(" ", "_"))
                intervals_data = get_intervals_data(session_key)
                if intervals_data:
                    # Parse the intervals data
                    intervals_reader = csv.DictReader(io.StringIO(intervals_data))
                    # Initialize a dictionary to hold intervals data for each driver
                    driver_intervals = {driver["driver_number"]: [] for driver in drivers}
                    for interval_row in intervals_reader:
                        driver_number = interval_row.get("driver_number")
                        if driver_number in driver_intervals:
                            driver_intervals[driver_number].append(interval_row)
                    # Write intervals data for each driver
                    for driver in drivers:
                        driver_number = driver["driver_number"]
                        driver_name = driver["name"]
                        driver_folder = os.path.join("drivers", driver_name, location_folder)
                        driver_data = driver_intervals.get(driver_number)
                        if driver_data:
                            # Prepare CSV data
                            output = io.StringIO()
                            writer = csv.DictWriter(output, fieldnames=intervals_reader.fieldnames)
                            writer.writeheader()
                            writer.writerows(driver_data)
                            write_csv(output.getvalue(), driver_folder, f"intervals_data_{session_name}.csv")
                        else:
                            print(f"No intervals data for driver {driver_name} in session {session_name}.")
                else:
                    print(f"Failed to retrieve intervals data for session {session_name}.")
    else:
        print(f"Failed to retrieve session data for year {year}.")

if __name__ == "__main__":
    main()
