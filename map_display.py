import folium
import requests
import time
import webbrowser
import os

BACKEND_URL = "http://127.0.0.1:5001/live"
MAP_FILE = "live_map.html"

def get_live_location():
    """Fetch latest GPS location from backend."""
    try:
        res = requests.get(BACKEND_URL, timeout=3).json()
        lat = res.get("lat")
        lng = res.get("lng")
        ts = res.get("timestamp")

        if lat is None or lng is None:
            print("[INFO] No GPS data yet.")
            return None, None, None

        return lat, lng, ts
    except Exception as e:
        print(f"[ERROR] Cannot reach backend: {e}")
        return None, None, None

def generate_map(lat, lng):
    """Generate a folium map with auto-refresh."""
    m = folium.Map(location=[lat, lng], zoom_start=17)

    folium.Marker(
        [lat, lng],
        popup="Live Bicycle Location",
        tooltip="Current Position"
    ).add_to(m)

    # Auto-refresh every 5 seconds (JS added to HTML)
    refresh_js = """
        <script>
            setTimeout(function(){
                location.reload();
            }, 5000);
        </script>
    """
    m.get_root().html.add_child(folium.Element(refresh_js))

    m.save(MAP_FILE)

def open_browser_once():
    """Open the map in the browser only if it is not already opened."""
    # Open in default browser
    file_path = "file://" + os.path.abspath(MAP_FILE)
    webbrowser.open(file_path, new=0)

def main():
    print("Opening live GPS map...")

    # Open browser the first time
    open_browser_once()

    while True:
        lat, lng, ts = get_live_location()

        if lat is not None and lng is not None:
            print(f"[UPDATE] {lat}, {lng} (ts={ts})")
            generate_map(lat, lng)

        # Browser will auto-refresh due to JS
        time.sleep(5)

if __name__ == "__main__":
    main()
