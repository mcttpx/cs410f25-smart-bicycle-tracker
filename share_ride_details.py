import uuid
from urllib.parse import urlencode

from data_visibility import can_view_shared_data
from results import build_results_summary

# Base URL used to build share links (replace with real UI domain from Michael)
BASE_SHARE_URL = "http://..."

# Stores tokens from shared ride data in-memory
_SHARED_RIDES = {}


# Create a share link for a completed ride
def create_share_link(ride_id, owner_id, ride_stats, approved_friends, distance_unit="km", speed_unit=None, duration_format="time"):
    # Unique token for current shared ride
    token = uuid.uuid4().hex

    # Summary results using units and time
    summary = build_results_summary(ride_stats, distance_unit=distance_unit, speed_unit=speed_unit, duration_format=duration_format)

    # Save shared ride info in memory
    _SHARED_RIDES[token] = {
        "ride_id": ride_id,
        "owner_id": owner_id,
        "summary": summary,
        "approved_friends": set(approved_friends)
    }

    # Creates a link with token as its query parameter
    query = urlencode({"token": token})
    return f"{BASE_SHARE_URL}?{query}"


# Looks up shared ride and checks permission
def get_shared_ride_for_viewer(token, viewer_id):
    record = _SHARED_RIDES.get(token)
    if not record:
        return None  # invalid or unknown token

    owner_id = record["owner_id"]
    extra_allowed = record["approved_friends"]

    # Only return data if viewer is allowed
    if not can_view_shared_data(owner_id, viewer_id, extra_allowed):
        return None

    return record["summary"]
