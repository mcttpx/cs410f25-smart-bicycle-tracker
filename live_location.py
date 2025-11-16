import requests
import time

# Your backend URL ( Flask server running on port 5001 )
BACKEND_URL = "http://127.0.0.1:5001/live"

def get_live_location():
    """
    Fetch the latest live GPS location from the backend.
    Returns a tuple: (lat, lng, timestamp)
    If backend fails → returns (None, None, None)
    """
    try:
        response = requests.get(BACKEND_URL, timeout=3)
        data = response.json()

        lat = data.get("lat")
        lng = data.get("lng")
        ts = data.get("timestamp")

        # If backend hasn't received data yet
        if lat is None or lng is None:
            print("[INFO] No GPS data received from backend yet.")
            return None, None, None

        return lat, lng, ts

    except Exception as e:
        print(f"[ERROR] Cannot reach backend: {e}")
        return None, None, None


# Optional: test the module directly
if __name__ == "__main__":
    while True:
        lat, lng, ts = get_live_location()
        print("Live Location →", lat, lng, ts)
        time.sleep(5)