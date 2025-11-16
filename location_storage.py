import json      # To read/write JSON files
import os        # To check if a file exists
from datetime import datetime, timedelta   # To work with dates and times

# File where all GPS locations will be saved
FILE = "data/locations.json"

# ---------------------------------------------------------------
# Reads the saved locations from the file.
# If the file does not exist or is broken → return an empty list.
# ---------------------------------------------------------------
def load_locations():

    # If the file does NOT exist → return empty list
    if not os.path.exists(FILE):
        return []

    # Try reading the file
    with open(FILE, "r") as f:
        try:
            return json.load(f)   # Load the JSON data
        except:
            return []             # If file is empty or invalid

# ---------------------------------------------------------------
# save_location()
# Saves a new GPS point into the file.
# Also removes locations older than 24 hours.
# ---------------------------------------------------------------
def save_location(loc):

    # Load old data from file
    locations = load_locations()

    # Add the new location to the list
    locations.append(loc)

    # Find the time 24 hours ago from right now
    cutoff = datetime.now() - timedelta(hours=24)

    # Keep ONLY locations from the last 24 hours
    filtered = []
    for entry in locations:
        entry_time = datetime.fromisoformat(entry["timestamp"])
        if entry_time >= cutoff:
            filtered.append(entry)

    # Save the filtered list back to the file
    with open(FILE, "w") as f:
        json.dump(filtered, f, indent=4)

    print("[US2] Location saved (only last 24 hours kept).")

# ---------------------------------------------------------------
# get_last_known()
# Returns the last saved GPS point.
# If no data exists → return None.
# ---------------------------------------------------------------
def get_last_known():

    # Load everything
    locations = load_locations()

    # If there is data → return last item
    # If empty → return None
    if locations:
        return locations[-1]
    else:
        return None