from datetime import timedelta

# Converts time into Hours, Minutes, Seconds
def format_duration_hms(seconds):
    if not seconds:
        return "0:00:00"
    return str(timedelta(seconds=int(seconds)))

# Duration conversion
def convert_duration(seconds, time_unit):
    if time_unit == "hours":
        return seconds / 3600.0
    if time_unit == "minutes":
        return seconds / 60.0
    if time_unit == "seconds":
        return seconds
    return format_duration_hms(seconds)

# Convert kilometers into chosen unit (km for kilometers or m for miles)
def convert_distance(dist_km, unit):
    if unit == "m":
        return dist_km * 0.621371, "m"
    return dist_km, "km"

# Compute speed in chosen unit (km/h or mph)
def compute_speed(dist_km, dur_sec, speed_unit):
    if dur_sec <= 0:
        return 0.0

    hours = dur_sec / 3600.0

    if speed_unit == "mph":
        return (dist_km * 0.621371) / hours
    return dist_km / hours

# Results summary using distance, speed, duration
def build_results_summary(ride_stats, distance_unit="km", speed_unit=None, duration_format="time"):
    dist_km = max(0.0, float(ride_stats.get("distance_km", 0.0)))
    dur_sec = max(0.0, float(ride_stats.get("duration_sec", 0.0)))

    # Auto-select speed unit to match distance unit
    if speed_unit is None:
        speed_unit = "mph" if distance_unit == "m" else "km/h"

    # Convert distance
    dist_value, dist_label = convert_distance(dist_km, distance_unit)

    # Compute speed
    if "avg_speed_kmh" in ride_stats and speed_unit == "km/h":
        speed_value = float(ride_stats["avg_speed_kmh"])
    else:
        speed_value = compute_speed(dist_km, dur_sec, speed_unit)

    # Convert duration
    dur_value = convert_duration(dur_sec, duration_format)

    # Final summary
    return {
        "distance": round(dist_value, 2),
        "distance_unit": dist_label,
        "avg_speed": round(speed_value, 2),
        "speed_unit": speed_unit,
        "duration": dur_value,
        "duration_format": duration_format,
        "start_time": ride_stats.get("start_time"),
        "end_time": ride_stats.get("end_time"),

        # Base-unit reference fields
        "distance_km": round(dist_km, 2),
        "avg_speed_kmh": compute_speed(dist_km, dur_sec, "km/h"),
        "duration_str": format_duration_hms(dur_sec)
    }
