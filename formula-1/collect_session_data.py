import requests
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
        data = response.text
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching session data from API: {e}")
        return None

def write_csv(data, folder, filename):
    folder_path = os.path.join("data", folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)
    with open(filepath, mode='w', newline='') as file:
        file.write(data)
        print(f"Session data written to {filepath}")

def main():
    year = "2024"  # Change the year as needed
    session_data = get_session_data(year)
    if session_data:
        write_csv(session_data, "grand-prix", "session_data.csv")
    else:
        print(f"Failed to retrieve session data for year {year}.")

if __name__ == "__main__":
    main()
