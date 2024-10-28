import subprocess
import os

# List of all your collect scripts
scripts = [
    "collect_intervals_data.py",
    "collect_laps_data.py",
    "collect_car_data.py",
    "collect_position_data.py",
    "collect_race_control_data.py",
    "collect_session_data.py",
    "collect_stints_data.py",
    "collect_pit_data.py",
    "collect_weather_data.py"
]

# Define the correct directory path where the scripts are located
# Assuming `run_all_collect_scripts.py` is also in `formula-1/scripts`
scripts_directory = os.path.dirname(__file__)  # Path to the `scripts` folder

# Run each script in the list
for script in scripts:
    script_path = os.path.join(scripts_directory, script)
    print(f"Running {script}...")
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"{script} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")
