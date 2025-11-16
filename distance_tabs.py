# ---------------------------------------------------------------
# Simulates selecting a tab: weekly, monthly, yearly.
# Displays the corresponding distance.
# ---------------------------------------------------------------
def view_tab(data, tab):
    if tab == "weekly":
        print(f"[US1] Weekly Distance: {data['weekly_distance']:.2f} km")
    elif tab == "monthly":
        print(f"[US1] Monthly Distance: {data['monthly_distance']:.2f} km")
    elif tab == "yearly":
        print(f"[US1] Yearly Distance: {data['yearly_distance']:.2f} km")
    else:
        print("[US1] Invalid tab selected.")