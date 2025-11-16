# ===============================================================
# SMART BICYCLE TRACKER – SPRINT_1 MAIN FILE
# Includes:
#   - User Story 1: Weekly Distance Tracking
#   - User Story 2: Live GPS Location Tracking
# ===============================================================

# -----------------------
# USER STORY 1 IMPORTS
# -----------------------
from User_Story_1_Cyclist.ride_simulator import simulate_ride
from User_Story_1_Cyclist.distance_summary import show_summary
from User_Story_1_Cyclist.distance_tabs import view_tab

# -----------------------
# USER STORY 2 IMPORTS
# -----------------------
from User_Story_2_Cyclist.live_location import start_tracking
from User_Story_2_Cyclist.location_storage import save_location
from User_Story_2_Cyclist.map_display import show_current_location

# ===============================================================
# DATA STORAGE FOR USER STORY 1
# Each ride updates weekly, monthly, and yearly totals.
# ===============================================================
data = {
    "weekly_distance": 0,
    "monthly_distance": 0,
    "yearly_distance": 0,
    "history": []
}

print("\n=== SMART BICYCLE TRACKER – SPRINT_1 DEMO (US1 + US2) ===\n")

# ===============================================================
# USER STORY 1 DEMO
# ===============================================================
print("\n----- USER STORY 1: WEEKLY DISTANCE TRACKING -----\n")

ride1_start = (42.3601, -71.0589)
ride1_end   = (42.3662, -71.0621)

simulate_ride(ride1_start, ride1_end, data)

show_summary(data)

view_tab(data, "weekly")
view_tab(data, "monthly")
view_tab(data, "yearly")

# ===============================================================
# USER STORY 2 DEMO (commented to avoid infinite loop)
# ===============================================================
# BASE_LAT = 42.3601
# BASE_LON = -71.0589
#
# try:
#     start_tracking(BASE_LAT, BASE_LON, save_location)
# except KeyboardInterrupt:
#     print("\n[US2] Tracking stopped by user.\n")
#     show_current_location()

print("\nSprint 1 Demonstration Complete (US1 executed).")
print("US2 is available but commented out to avoid infinite loop.\n")