from datetime import datetime
from utils.calculateDistance import calculate_distance

# ---------------------------------------------------------------
# Simulates a bicycle ride between two GPS points.
# Uses Haversine formula to calculate actual distance.
# Updates weekly, monthly, yearly totals.
# Stores ride in history list.
# ---------------------------------------------------------------
def simulate_ride(start, end, data):
    # Calculate distance in km
    distance = calculate_distance(start[0], start[1], end[0], end[1])

    # Update totals
    data["weekly_distance"] += distance
    data["monthly_distance"] += distance
    data["yearly_distance"] += distance

    # Create record of the ride
    ride_record = {
        "distance_km": round(distance, 2),
        "start": start,
        "end": end,
        "time": datetime.now().isoformat()
    }

    # Add ride to history
    data["history"].append(ride_record)

    print(f"[US1] Ride completed: {distance:.2f} km")

    return distance