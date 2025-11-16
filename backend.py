from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import sqlite3

app = Flask(__name__)
CORS(app)

from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

# Haversine distance formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# ---------------------------------------
# DATABASE SETUP
# ---------------------------------------
def init_db():
    conn = sqlite3.connect("gps_data.db")
    c = conn.cursor()

    # Store GPS points
    c.execute("""
        CREATE TABLE IF NOT EXISTS live_location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lng REAL,
            timestamp INTEGER
        )
    """)

    # Store daily distance totals
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_distance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            distance REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------------------------------
# 1. ESP32 POSTS GPS DATA HERE
# ---------------------------------------
@app.route("/update", methods=["POST"])
def update_location():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")
    ts = int(time.time())

    conn = sqlite3.connect("gps_data.db")
    c = conn.cursor()

    # 1. Insert new point
    c.execute("INSERT INTO live_location (lat, lng, timestamp) VALUES (?, ?, ?)",
              (lat, lng, ts))

    # 2. Fetch last 2 points to compute incremental distance
    c.execute("SELECT lat, lng FROM live_location ORDER BY id DESC LIMIT 2")
    rows = c.fetchall()

    if len(rows) == 2:
        (lat2, lon2), (lat1, lon1) = rows   # latest is lat1/lon1
        distance_increment = haversine(lat1, lon1, lat2, lon2)
    else:
        distance_increment = 0.0

    print("Increment distance:", distance_increment)

    # 3. Update today's total
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT distance FROM daily_distance WHERE date=?", (today,))
    row = c.fetchone()

    if row:
        new_total = row[0] + distance_increment
        c.execute("UPDATE daily_distance SET distance=? WHERE date=?", (new_total, today))
    else:
        c.execute("INSERT INTO daily_distance (date, distance) VALUES (?, ?)",
                  (today, distance_increment))

    conn.commit()
    conn.close()

    print(f"GPS UPDATE → lat:{lat}, lng:{lng}, time:{ts}")
    return jsonify({"status": "ok"})

# ---------------------------------------
# 2. GET latest coordinate
# ---------------------------------------
@app.route("/live", methods=["GET"])
def get_live_location():
    conn = sqlite3.connect("gps_data.db")
    c = conn.cursor()
    c.execute("SELECT lat, lng, timestamp FROM live_location ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        return jsonify({"lat": row[0], "lng": row[1], "timestamp": row[2]})
    else:
        return jsonify({"lat": None, "lng": None, "timestamp": None})

# ---------------------------------------
# 3. WEEKLY SUMMARY ENDPOINT
# ---------------------------------------
@app.route("/weekly_summary", methods=["GET"])
def weekly_summary():
    conn = sqlite3.connect("gps_data.db")
    c = conn.cursor()

    c.execute("""
        SELECT date, distance FROM daily_distance
        ORDER BY date DESC
        LIMIT 7
    """)
    rows = c.fetchall()
    conn.close()

    summary = [{"date": d, "distance_km": round(dist, 2)} for d, dist in rows]
    return jsonify(summary)

# ---------------------------------------
# TEST HAVERSINE FUNCTION
# ---------------------------------------
print("Testing Haversine...")
lat1, lon1 = 42.3601, -71.0589
lat2, lon2 = 42.3736, -71.1097
dist_km = haversine(lat1, lon1, lat2, lon2)
print("Distance (km):", dist_km)

# ---------------------------------------
# RUN SERVER
# ---------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
