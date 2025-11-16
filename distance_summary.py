import requests

BACKEND_URL = "http://127.0.0.1:5001/weekly_summary"

def get_weekly_distance():
    """Fetch the last 7 days of distance data from backend."""
    try:
        response = requests.get(BACKEND_URL, timeout=3)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching weekly distance:", e)
        return []

def print_summary(summary):
    """Print weekly distance in clean readable format."""
    print("\n============================")
    print("   WEEKLY DISTANCE SUMMARY  ")
    print("============================\n")

    if not summary:
        print("No distance data recorded yet.\n")
        return

    total = 0

    for entry in summary:
        date = entry["date"]
        dist = entry["distance_km"]
        total += dist
        print(f"{date}   →   {dist} km")

    print("\n----------------------------")
    print(f"TOTAL (last 7 days): {round(total, 2)} km")
    print("----------------------------\n")

if __name__ == "__main__":
    summary = get_weekly_distance()
    print_summary(summary)
